import os
import numpy as np
from sentence_transformers import SentenceTransformer
import faiss

# 加载 Sentence-BERT 模型
model = SentenceTransformer('paraphrase-MiniLM-L6-v2')

# 假设有一些文本文件在 'documents/' 目录中
document_dir = "E:\\Codefield\\CODE_C\\Git\\ArkFS\\src\\file_system_resembling_shell\\target_folder"

# 读取所有文本文件
documents = []
filenames = []
file_embeddings = []

for filename in os.listdir(document_dir):
    if filename.endswith('.txt'):
        with open(os.path.join(document_dir, filename), 'r', encoding='utf-8') as f:
            content = f.read()
            documents.append(content)
            filenames.append(filename)
            # 将文件名转化为嵌入向量
            file_embedding = model.encode([filename])[0]
            file_embeddings.append(file_embedding)

# 将所有文档转化为嵌入向量
document_embeddings = model.encode(documents)

# 拼接文件名和文档内容的嵌入向量
combined_embeddings = np.hstack([file_embeddings, document_embeddings])

# 使用 FAISS 构建索引
dimension = combined_embeddings.shape[1]
index = faiss.IndexFlatL2(dimension)
index.add(combined_embeddings)

# 查询处理
def search(query, top_k=5):
    query_embedding = model.encode([query])[0]
    # 拼接查询的文件名和内容嵌入向量（假设查询不含文件名，文件名部分置零）
    query_embedding_full = np.hstack([np.zeros(file_embeddings[0].shape), query_embedding])
    D, I = index.search(np.array([query_embedding_full]), top_k)
    
    results = []
    for i in I[0]:
        results.append(filenames[i])
    
    return results

# 示例查询
query = "草"
results = search(query)

print("搜索结果：")
for result in results:
    print(result)
