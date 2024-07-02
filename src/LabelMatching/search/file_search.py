import torch
import clip
import faiss
import os
import json
import numpy as np
from PIL import Image
from transformers import XLMRobertaTokenizer, XLMRobertaModel
from datetime import datetime

def load_models(device):
    clip_model, clip_preprocess = clip.load("ViT-B/32", device=device)
    model_name = "xlm-roberta-base"
    tokenizer = XLMRobertaTokenizer.from_pretrained(model_name)
    xlm_model = XLMRobertaModel.from_pretrained(model_name).to(device)
    return clip_model, clip_preprocess, tokenizer, xlm_model

def process_file(file_path, clip_model, clip_preprocess, tokenizer, xlm_model, image_features, text_features, image_paths, text_paths, file_info, device):
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
                outputs = xlm_model(**inputs)
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
    clip_model, clip_preprocess, tokenizer, xlm_model = load_models(device)

    image_features = []
    text_features = []
    image_paths = []
    text_paths = []
    file_info = []

    for root, _, files in os.walk(file_dir):
        for fname in files:
            process_file(os.path.join(root, fname), clip_model, clip_preprocess, tokenizer, xlm_model, image_features, text_features, image_paths, text_paths, file_info, device)

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

    output_dir = os.path.join(file_dir, "..", "processed_data")
    os.makedirs(output_dir, exist_ok=True)
    output_file = os.path.join(output_dir, "processed_data.json")
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump({
            "file_info": file_info
        }, f, indent=4, ensure_ascii=False)

    query_input = clip.tokenize([query]).to(device)
    with torch.no_grad():
        query_feature_clip = clip_model.encode_text(query_input).cpu().numpy()
    query_feature_clip /= np.linalg.norm(query_feature_clip)

    inputs = tokenizer(query, return_tensors="pt", max_length=512, truncation=True, padding=True).to(device)
    with torch.no_grad():
        outputs = xlm_model(**inputs)
    query_feature_xlm = outputs.last_hidden_state.mean(dim=1).cpu().numpy()
    query_feature_xlm /= np.linalg.norm(query_feature_xlm)

    return image_index, text_index, image_paths, text_paths, file_info, query_feature_clip, query_feature_xlm

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

def search_files(image_index, text_index, image_paths, text_paths, file_info, query_feature_clip, query_feature_xlm, modified_time_start=None, modified_time_end=None, k=5):
    image_results = search_images(image_index, image_paths, query_feature_clip, k)
    text_results = search_texts(text_index, text_paths, query_feature_xlm, k)

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
               (not modified_time_end or modified_time <= datetime.fromisoformat(modified_time_end)) and (score > 0.98):
                filtered_results["text_results"].append(path)

    filtered_results["image_results"].append(len(filtered_results["image_results"]))
    filtered_results["text_results"].append(len(filtered_results["text_results"]))

    return filtered_results["image_results"], filtered_results["text_results"]

def my_search(modified_time, content, target_folder):
    os.environ["KMP_DUPLICATE_LIB_OK"] = "TRUE"
    image_index, text_index, image_paths, text_paths, file_info, query_feature_clip, query_feature_xlm = process_files_query(target_folder, content)
    modified_time_start = modified_time[0] or None
    modified_time_end = modified_time[1] or None
    image_results, text_results = search_files(image_index, text_index, image_paths, text_paths, file_info, query_feature_clip, query_feature_xlm, modified_time_start, modified_time_end, k=10)

    return image_results or None, text_results or None
