import torch
import clip
import faiss
import os
import numpy as np
from PIL import Image
from datetime import datetime
from transformers import T5Tokenizer, T5ForConditionalGeneration

def load_models(device):
    clip_model, clip_preprocess = clip.load("ViT-B/32", device=device)
    t5_tokenizer = T5Tokenizer.from_pretrained("t5-small")
    t5_model = T5ForConditionalGeneration.from_pretrained("t5-small").to(device)
    return clip_model, clip_preprocess, t5_tokenizer, t5_model

def summarize_text(text, tokenizer, model, device):
    text = "summarize" + text 
    input_ids = tokenizer.encode(text, return_tensors="pt", max_length=512, truncation=True).to(device)
    summary_ids = model.generate(input_ids, max_length=60, min_length=30, length_penalty=2.0, num_beams=4, early_stopping=True)
    summary = tokenizer.decode(summary_ids[0], skip_special_tokens=True)
    return summary

def process_file(file_path, clip_model, clip_preprocess, tokenizer, summarization_model, image_features, text_features, image_paths, text_paths, file_info, device):
        if file_path.lower().endswith(('.png', '.jpg', '.jpeg', '.bmp', '.gif')):
            image = clip_preprocess(Image.open(file_path)).unsqueeze(0).to(device)
            with torch.no_grad():
                feature = clip_model.encode_image(image)
                image_features.append(feature.cpu().numpy())
                image_paths.append(file_path)
        elif file_path.lower().endswith('.txt'):
            with open(file_path, 'r', encoding='utf-8') as f:
                text = f.read().strip()
            try:
                text_tokens = clip.tokenize([text]).to(device)
                with torch.no_grad():
                    feature = clip_model.encode_text(text_tokens)
                text_features.append(feature.cpu().numpy())
                text_paths.append(file_path)
            except Exception as clip_error:
                try:
                    # 生成摘要
                    summary = summarize_text(text, tokenizer, summarization_model, device)
                    summary_tokens = clip.tokenize([summary]).to(device)
                    with torch.no_grad():
                        feature = clip_model.encode_text(summary_tokens)
                    text_features.append(feature.cpu().numpy())
                    text_paths.append(file_path)
                except Exception as summary_error:
                    return

        file_stat = os.stat(file_path)
        modified_time = datetime.fromtimestamp(file_stat.st_mtime).isoformat()
        file_info.append({
            "file_path": file_path,
            "modified_time": modified_time,
            "file_name": os.path.basename(file_path)
        })


def process_files_query(file_dir, query):
    device = "cuda" if torch.cuda.is_available() else "cpu"
    clip_model, clip_preprocess, t5_tokenizer, t5_model = load_models(device)

    image_features = []
    text_features = []
    image_paths = []
    text_paths = []
    file_info = []

    for root, _, files in os.walk(file_dir):
        for fname in files:
            process_file(os.path.join(root, fname), clip_model, clip_preprocess, t5_tokenizer, t5_model, image_features, text_features, image_paths, text_paths, file_info, device)

    image_features = np.vstack(image_features) if image_features else np.array([])
    if image_features.size > 0:
        image_features /= np.linalg.norm(image_features, axis=1, keepdims=True)

    text_features = np.vstack(text_features) if text_features else np.array([])
    if text_features.size > 0:
        text_features /= np.linalg.norm(text_features, axis=1, keepdims=True)

    image_index = faiss.IndexFlatIP(image_features.shape[1]) if image_features.size > 0 else None
    if image_index:
        image_index.add(image_features)

    text_index = faiss.IndexFlatIP(text_features.shape[1]) if text_features.size > 0 else None
    if text_index:
        text_index.add(text_features)
        
    # if len(query) > 70:
    #     query = query[:70]  # 截断查询到70个字符
    query_input = clip.tokenize([query]).to(device)
    with torch.no_grad():
        query_feature = clip_model.encode_text(query_input).cpu().numpy()
    query_feature /= np.linalg.norm(query_feature)

    return image_index, text_index, image_paths, text_paths, file_info, query_feature

def search_images(image_index, image_paths, query_feature, k=5):
    if not image_index:
        return []
    D, I = image_index.search(query_feature, k)
    return [(image_paths[i], D[0][j]) for j, i in enumerate(I[0])]

def search_texts(text_index, text_paths, query_feature, k=5):
    if not text_index:
        return []
    D, I = text_index.search(query_feature, k)
    return [(text_paths[i], D[0][j]) for j, i in enumerate(I[0])]

def search_files(image_index, text_index, image_paths, text_paths, file_info, query_feature, modified_time_start=None, modified_time_end=None, k=5):
    image_results = search_images(image_index, image_paths, query_feature, k)
    text_results = search_texts(text_index, text_paths, query_feature, k)

    filtered_results = {
        "image_results": [],
        "text_results": [],
    }

    for path, score in image_results:
        info = next((info for info in file_info if info['file_path'] == path), None)
        if info:
            modified_time = datetime.fromisoformat(info['modified_time'])
            if (not modified_time_start or modified_time >= datetime.fromisoformat(modified_time_start)) and \
               (not modified_time_end or modified_time <= datetime.fromisoformat(modified_time_end)) and (score > 0.20):
                filtered_results["image_results"].append(path)

    for path, score in text_results:
        info = next((info for info in file_info if info['file_path'] == path), None)
        if info:
            modified_time = datetime.fromisoformat(info['modified_time'])
            if (not modified_time_start or modified_time >= datetime.fromisoformat(modified_time_start)) and \
               (not modified_time_end or modified_time <= datetime.fromisoformat(modified_time_end)) and (score > 0.80):
                filtered_results["text_results"].append(path)

    return filtered_results["image_results"], filtered_results["text_results"]

def simple_search(modified_time, target_folder):
    image_results = []
    text_results = []
    modified_time_start = modified_time[0] or None
    modified_time_end = modified_time[1] or None
    for root, _, files in os.walk(target_folder):
        for fname in files:
            file_path = os.path.join(root, fname)
            file_stat = os.stat(file_path)
            file_modified_time = datetime.fromtimestamp(file_stat.st_mtime).isoformat()
            if(fname.lower().endswith(('.png', '.jpg', '.jpeg', '.bmp', '.gif'))):
                if (not modified_time_start or file_modified_time >= modified_time_start) and \
                (not modified_time_end or file_modified_time <= modified_time_end):
                    image_results.append(file_path)
            elif(fname.lower().endswith('.txt')):
                if (not modified_time_start or file_modified_time >= modified_time_start) and \
                (not modified_time_end or file_modified_time <= modified_time_end):
                    text_results.append(file_path)
    
    return image_results, text_results
                   
# opcode = [modified_time, content, target_folder]
def my_search(opcode):
    os.environ["KMP_DUPLICATE_LIB_OK"] = "TRUE"
    modified_time = opcode[0]
    content = opcode[1]
    target_folder = opcode[2]
    if not content:
        image_results, text_results = simple_search(modified_time, target_folder)
    else:
        image_index, text_index, image_paths, text_paths, file_info, query_feature = process_files_query(target_folder, content)
        modified_time_start = modified_time[0] or None
        modified_time_end = modified_time[1] or None
        image_results, text_results = search_files(image_index, text_index, image_paths, text_paths, file_info, query_feature, modified_time_start, modified_time_end, k=10)

    return [image_results, text_results]
