import faiss
from sentence_transformers import SentenceTransformer
import numpy as np

import warnings    #消除未知的警报
warnings.filterwarnings("ignore", category=FutureWarning)

# 读取文本文件中的数据
def read_documents(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        documents = file.readlines()
    return [doc.strip() for doc in documents]

# 从文件读取文档
documents = read_documents('documents.txt')


# 初始化句子嵌入模型
embedding_model = SentenceTransformer('all-MiniLM-L6-v2')


# 文本向量化
document_embeddings = embedding_model.encode(documents)

# 生成嵌入
embedding_matrix = np.array(document_embeddings)

# 构建Faiss索引
index = faiss.IndexFlatL2(embedding_matrix.shape[1])
index.add(embedding_matrix)

# 保存索引到文件
faiss.write_index(index, "index.faiss")

# 查询索引函数
def query_index(query_text, index, embedding_model, top_k=5):
    query_embedding = embedding_model.encode([query_text])
    D, I = index.search(query_embedding, k=top_k)  # 查找最相似的top_k个文档
    return I, D

# 示例查询
query_text =""
query_text=input("请输入查询文本：")

I, D = query_index(query_text, index, embedding_model)

print("Top {} documents indices:".format(len(I[0])))
print(I[0])  # 输出最相似的文档索引
print("Distances:")
print(D[0])  # 输出对应的距离

print("\n")

##对文档进行聚类

from sklearn.cluster import KMeans

# 设置聚类数量
num_clusters = 5  # 假设将文档分成5类

# 进行K-means聚类
kmeans = KMeans(n_clusters=num_clusters, random_state=0)
kmeans.fit(document_embeddings)

# 获取每个文档的聚类标签
labels = kmeans.labels_

# 创建每个聚类的文档列表
clustered_documents = [[] for _ in range(num_clusters)]
for doc_index, label in enumerate(labels):
    clustered_documents[label].append(documents[doc_index])

# 输出每个聚类的文档
for cluster_index, cluster_docs in enumerate(clustered_documents):
    print(f"Cluster {cluster_index}:")
    for doc in cluster_docs:
        print(f"  - {doc}")