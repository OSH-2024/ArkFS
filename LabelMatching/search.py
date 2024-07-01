import os
import torch
import clip
from PIL import Image
import numpy as np
import faiss

os.environ["KMP_DUPLICATE_LIB_OK"] = "TRUE"
# 加载模型和预处理函数
device = "cuda" if torch.cuda.is_available() else "cpu"
model, preprocess = clip.load("ViT-B/32", device=device)

# 文件目录
file_dir = r"ArkFS\\file_system_resembling_shell\\target_folder"


# 初始化特征列表和文件路径列表
features = []
file_paths = []

# 遍历目录，处理文本和图像文件
for fname in os.listdir(file_dir):
    file_path = os.path.join(file_dir, fname)
    if fname.lower().endswith(('.png', '.jpg', '.jpeg', '.bmp', '.gif')):
        # 处理图像文件
        image = preprocess(Image.open(file_path)).unsqueeze(0).to(device)
        with torch.no_grad():
            feature = model.encode_image(image)
        features.append(feature.cpu().numpy())
        file_paths.append(file_path)
    # elif fname.lower().endswith('.txt'):
    #     # 处理文本文件
    #     with open(file_path, 'r') as f:
    #         text = f.read().strip()
    #     text_input = clip.tokenize([text]).to(device)
    #     with torch.no_grad():
    #         feature = model.encode_text(text_input)
    #     features.append(feature.cpu().numpy())
    #     file_paths.append(file_path)

# 将特征向量列表转换为NumPy数组，并归一化
features = np.vstack(features)
features /= np.linalg.norm(features, axis=1, keepdims=True)

# 创建FAISS索引并添加特征
index = faiss.IndexFlatIP(features.shape[1])
index.add(features)

# 定义文件查找函数
def search_files(query, k=5):
    query_input = clip.tokenize([query]).to(device)
    with torch.no_grad():
        query_feature = model.encode_text(query_input).cpu().numpy()
    query_feature /= np.linalg.norm(query_feature)
    
    D, I = index.search(query_feature, k)
    return [(file_paths[i], D[0][j]) for j, i in enumerate(I[0])]

# 示例查询
query = "grass"  # 输入查询文本
results = search_files(query, k=5)  # 查找最相似的5个文件

# 打印结果
for file_path, score in results:
    print(f"File: {file_path}, Similarity: {score:.4f}")
