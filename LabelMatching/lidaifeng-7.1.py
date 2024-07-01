import os
import torch
import clip
from PIL import Image
import numpy as np
import faiss
from datetime import datetime

# 设置环境变量以允许重复的 OpenMP 库
os.environ["KMP_DUPLICATE_LIB_OK"] = "TRUE"

# 加载 CLIP 模型和预处理函数
device = "cuda" if torch.cuda.is_available() else "cpu"
model, preprocess = clip.load("ViT-B/32", device=device)

# 获取当前工作目录
current_dir = os.getcwd()

# 文件目录和新文件夹路径
file_dir = os.path.join(current_dir, "target_folder")
output_dir = os.path.join(current_dir, "target_folder")
os.makedirs(output_dir, exist_ok=True)

# 初始化特征列表、文件路径列表和文件信息列表
features = []
file_paths = []
file_info = []

# 处理目录中的文件
for fname in os.listdir(file_dir):
    file_path = os.path.join(file_dir, fname)
    try:
        if fname.lower().endswith(('.png', '.jpg', '.jpeg', '.bmp', '.gif')):
            # 处理图像文件
            image = preprocess(Image.open(file_path)).unsqueeze(0).to(device)
            with torch.no_grad():
                feature = model.encode_image(image)
                features.append(feature.cpu().numpy())
                file_paths.append(file_path)
        
        # 记录文件信息：文件路径、最后修改时间、文件名
        file_stat = os.stat(file_path)
        modified_time = datetime.fromtimestamp(file_stat.st_mtime).isoformat()
        file_info.append(f"{file_path}\t{modified_time}\t{fname}")

    except Exception as e:
        print(f"Error processing file {file_path}: {e}")

# 将特征向量列表转换为 NumPy 数组并归一化
features = np.vstack(features)
features /= np.linalg.norm(features, axis=1, keepdims=True)

# 创建 FAISS 索引并添加特征
index = faiss.IndexFlatIP(features.shape[1])
index.add(features)

# 保存特征向量和文件信息到文件
output_file = os.path.join(output_dir, "processed_data.txt")
np.savetxt(output_file, features, delimiter='\t')

# 保存文件信息到文本文件
file_info_output = os.path.join(output_dir, "file_info.txt")
with open(file_info_output, 'w') as f:
    for info in file_info:
        f.write(info + '\n')

print(f"Processed data saved to: {output_file}")
print(f"File info saved to: {file_info_output}")

# 定义文件搜索函数
def search_files(query, k=5):
    query_input = clip.tokenize([query]).to(device)
    with torch.no_grad():
        query_feature = model.encode_text(query_input).cpu().numpy()
    query_feature /= np.linalg.norm(query_feature)

    D, I = index.search(query_feature, k)
    return [(file_paths[i], D[0][j]) for j, i in enumerate(I[0])]

# 主循环进行查询
while True:
    query = input("输入查询语句（或输入 'exit' 退出）: ")
    if query.lower() == 'exit':
        break
    results = search_files(query, k=5)
    for file_path, score in results:
        print(f"文件: {file_path}, 相似度: {score:.4f}")
