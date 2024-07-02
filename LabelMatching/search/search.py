import torch
import clip
import faiss
import os
import json
import numpy as np
from PIL import Image
from transformers import XLMRobertaTokenizer, XLMRobertaModel
from datetime import datetime

def process_files_query(file_dir, image_features, text_features, image_paths, text_paths, file_info, query):
    # 加载 CLIP 模型和预处理函数
    device = "cuda" if torch.cuda.is_available() else "cpu"
    clip_model, clip_preprocess = clip.load("ViT-B/32", device=device)

    # 加载 XLM-R 模型和分词器（用于文本处理）
    model_name = "xlm-roberta-base"
    tokenizer = XLMRobertaTokenizer.from_pretrained(model_name)
    xlm_model = XLMRobertaModel.from_pretrained(model_name).to(device)
    # 处理目录中的文件
    for fname in os.listdir(file_dir):
        file_path = os.path.join(file_dir, fname)
        try:
            if fname.lower().endswith(('.png', '.jpg', '.jpeg', '.bmp', '.gif')):
                # 处理图像文件
                image = clip_preprocess(Image.open(file_path)).unsqueeze(0).to(device)
                with torch.no_grad():
                    feature = clip_model.encode_image(image)
                    image_features.append(feature.cpu().numpy())
                    image_paths.append(file_path)
            elif fname.lower().endswith('.txt'):
                # 处理文本文件
                with open(file_path, 'r', encoding='utf-8') as f:
                    text = f.read().strip()
                inputs = tokenizer(text, return_tensors="pt", max_length=512, truncation=True, padding=True).to(device)
                with torch.no_grad():
                    outputs = xlm_model(**inputs)
                feature = outputs.last_hidden_state.mean(dim=1)
                text_features.append(feature.cpu().numpy())
                text_paths.append(file_path)

            # 记录文件信息：文件路径、最后修改时间、文件名
            file_stat = os.stat(file_path)
            modified_time = datetime.fromtimestamp(file_stat.st_mtime).isoformat()
            file_info.append({
                "file_path": file_path,
                "modified_time": modified_time,
                "file_name": fname
            })
        except Exception as e:
            print(f"Error processing file {file_path}: {e}")

    # 将特征向量列表转换为 NumPy 数组并归一化
    if image_features:
        image_features = np.vstack(image_features)
        if image_features.shape[0] > 0:
            image_features /= np.linalg.norm(image_features, axis=1, keepdims=True)
        else:
            image_features = np.array([])
    else:
        image_features = np.array([])

    if text_features:
        text_features = np.vstack(text_features)
        if text_features.shape[0] > 0:
            text_features /= np.linalg.norm(text_features, axis=1, keepdims=True)
        else:
            text_features = np.array([])
    else:
        text_features = np.array([])


    # 创建 FAISS 索引并添加特征
    image_index = faiss.IndexFlatIP(image_features.shape[1]) if image_features.size > 0 else None
    if image_index:
        image_index.add(image_features)

    text_index = faiss.IndexFlatIP(text_features.shape[1]) if text_features.size > 0 else None
    if text_index:
        text_index.add(text_features)

    # 新文件夹路径
    output_dir = os.path.join(file_dir, "..", "processed_data")
    os.makedirs(output_dir, exist_ok=True)
    # 保存特征向量和文件信息到文件
    output_file = os.path.join(output_dir, "processed_data.json")
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump({
            # "image_features": image_features.tolist(),
            # "text_features": text_features.tolist(),
            "file_info": file_info
        }, f, indent=4, ensure_ascii=False)
        
    # 使用 CLIP 对查询进行编码
    query_input = clip.tokenize([query]).to(device)
    with torch.no_grad():
        query_feature_clip = clip_model.encode_text(query_input).cpu().numpy()
    query_feature_clip /= np.linalg.norm(query_feature_clip)

    # 使用 XLM-R 对查询进行编码
    inputs = tokenizer(query, return_tensors="pt", max_length=512, truncation=True, padding=True).to(device)
    with torch.no_grad():
        outputs = xlm_model(**inputs)
    query_feature_xlm = outputs.last_hidden_state.mean(dim=1).cpu().numpy()
    query_feature_xlm /= np.linalg.norm(query_feature_xlm)

    return image_index, text_index, image_paths, text_paths, file_info, query_feature_clip, query_feature_xlm

# 定义文件搜索函数
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
    # 根据查询特征在各自的索引中搜索
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
    # 设置环境变量以允许重复的 OpenMP 库
    os.environ["KMP_DUPLICATE_LIB_OK"] = "TRUE"
    # 初始化特征列表、文件路径列表和文件信息列表
    image_features = []
    text_features = []
    image_paths = []
    text_paths = []
    file_info = []
    # 文件目录
    file_dir = target_folder  
    image_index, text_index, image_paths, text_paths, file_info, query_feature_clip, query_feature_xlm = process_files_query(file_dir, image_features, text_features, image_paths, text_paths, file_info, content)
    #ISO 格式，例如 2024-07-01T23:59:59
    modified_time_start = modified_time[0] or None
    modified_time_end = modified_time[1] or None
    image_results, text_results = search_files(image_index, text_index, image_paths, text_paths, file_info, query_feature_clip, query_feature_xlm, modified_time_start, modified_time_end, k=10)
    
    return image_results or None, text_results or None

image_results, text_results = my_search([None, None], "grass", "E:\\Codefield\\CODE_C\\Git\\ArkFS\\file_system_resembling_shell\\target_folder")
print (image_results)