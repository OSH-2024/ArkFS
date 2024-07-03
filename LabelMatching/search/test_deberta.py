import torch
import clip
import faiss
import os
import numpy as np
from PIL import Image
from transformers import DebertaTokenizer, DebertaModel
from datetime import datetime

def load_models(device):
    clip_model, clip_preprocess = clip.load("ViT-B/32", device=device)
    model_name = "microsoft/deberta-base"
    tokenizer = DebertaTokenizer.from_pretrained(model_name)
    deberta_model = DebertaModel.from_pretrained(model_name).to(device)
    return clip_model, clip_preprocess, tokenizer, deberta_model

def process_file(file_path, clip_model, clip_preprocess, tokenizer, deberta_model, image_features, text_features, image_paths, text_paths, file_info, device):
    try:
        if file_path.lower().endswith(('.png', '.jpg', '.jpeg', '.bmp', '.gif')):
            image = clip_preprocess(Image.open(file_path)).unsqueeze(0).to(device)
            with torch.no_grad():
                feature = clip_model.encode_image(image)
                image_features.append(feature.cpu().numpy())
                image_paths.append(file_path)
        elif file_path.lower().endswith('.txt'):
            with open(file_path, 'r', encoding='utf-8') as f:
                text = f.read().strip()
            inputs = tokenizer(text, return_tensors="pt", max_length=512, truncation=True, padding=True).to(device)
            with torch.no_grad():
                outputs = deberta_model(**inputs)
            feature = outputs.last_hidden_state.mean(dim=1)
            text_features.append(feature.cpu().numpy())
            text_paths.append(file_path)

        file_stat = os.stat(file_path)
        modified_time = datetime.fromtimestamp(file_stat.st_mtime).isoformat()
        file_info.append({
            "file_path": file_path,
            "modified_time": modified_time,
            "file_name": os.path.basename(file_path)
        })
    except Exception as e:
        print(f"Error processing file {file_path}: {e}")

def process_files_query(file_dir, query):
    device = "cuda" if torch.cuda.is_available() else "cpu"
    clip_model, clip_preprocess, tokenizer, deberta_model = load_models(device)

    image_features = []
    text_features = []
    image_paths = []
    text_paths = []
    file_info = []

    for root, _, files in os.walk(file_dir):
        for fname in files:
            process_file(os.path.join(root, fname), clip_model, clip_preprocess, tokenizer, deberta_model, image_features, text_features, image_paths, text_paths, file_info, device)

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
        
    query_input = clip.tokenize([query]).to(device)
    with torch.no_grad():
        query_feature_clip = clip_model.encode_text(query_input).cpu().numpy()
    query_feature_clip /= np.linalg.norm(query_feature_clip)

    inputs = tokenizer(query, return_tensors="pt", max_length=512, truncation=True, padding=True).to(device)
    with torch.no_grad():
        outputs = deberta_model(**inputs)
    query_feature_deberta = outputs.last_hidden_state.mean(dim=1).cpu().numpy()
    query_feature_deberta /= np.linalg.norm(query_feature_deberta)

    return image_index, text_index, image_paths, text_paths, file_info, query_feature_clip, query_feature_deberta

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

def search_files(image_index, text_index, image_paths, text_paths, file_info, query_feature_clip, query_feature_deberta, modified_time_start=None, modified_time_end=None, k=5):
    image_results = search_images(image_index, image_paths, query_feature_clip, k)
    text_results = search_texts(text_index, text_paths, query_feature_deberta, k)

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
               (not modified_time_end or modified_time <= datetime.fromisoformat(modified_time_end)):
                filtered_results["text_results"].append((path, score))

    filtered_results["image_results"].append(len(filtered_results["image_results"]))
    filtered_results["text_results"].append(len(filtered_results["text_results"]))

    return filtered_results["image_results"], filtered_results["text_results"]

def simple_search(modified_time, target_folder):
    image_results = []
    text_results = []
    modified_time_start = modified_time[0] or None
    modified_time_end = modified_time[1] or None
    for root, _, files in os.walk(target_folder):
        for fname in files:
            if(fname.lower().endswith(('.png', '.jpg', '.jpeg', '.bmp', '.gif'))):
                if (not modified_time_start or datetime.fromisoformat(modified_time) >= datetime.fromisoformat(modified_time_start)) and \
                (not modified_time_end or datetime.fromisoformat(modified_time) <= datetime.fromisoformat(modified_time_end)):
                    image_results.append(os.path.join(root, fname))
            elif(fname.lower().endswith('.txt')):
                if (not modified_time_start or datetime.fromisoformat(modified_time) >= datetime.fromisoformat(modified_time_start)) and \
                (not modified_time_end or datetime.fromisoformat(modified_time) <= datetime.fromisoformat(modified_time_end)):
                    text_results.append(os.path.join(root, fname))
    
    image_results.append(len(image_results))
    text_results.append(len(text_results))
    return image_results, text_results
                   

def my_search(modified_time, content, target_folder):
    if not content:
        image_results, text_results = simple_search(modified_time, target_folder)
    else:
        os.environ["KMP_DUPLICATE_LIB_OK"] = "TRUE"
        image_index, text_index, image_paths, text_paths, file_info, query_feature_clip, query_feature_deberta = process_files_query(target_folder, content)
        modified_time_start = modified_time[0] or None
        modified_time_end = modified_time[1] or None
        image_results, text_results = search_files(image_index, text_index, image_paths, text_paths, file_info, query_feature_clip, query_feature_deberta, modified_time_start, modified_time_end, k=10)

    return image_results, text_results