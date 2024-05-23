import os
from sentence_transformers import SentenceTransformer
from sklearn.cluster import KMeans
from sklearn.feature_extraction.text import TfidfVectorizer
import numpy as np

# 读取文本文件中的数据
def read_documents(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        documents = file.readlines()
    return [doc.strip() for doc in documents]

# 从文件读取文档
documents = read_documents('documents.txt')

# 加载预训练模型
embedding_model = SentenceTransformer('all-MiniLM-L6-v2')

# 文本向量化
document_embeddings = embedding_model.encode(documents)

# 设置聚类数量
num_clusters = 5  # 假设您想将文档分成5类

# 进行K-means聚类
kmeans = KMeans(n_clusters=num_clusters, random_state=0)
kmeans.fit(document_embeddings)

# 获取每个文档的聚类标签
labels = kmeans.labels_

# 获取每个聚类的中心点（质心）
cluster_centers = kmeans.cluster_centers_

# 创建每个聚类的文档列表
clustered_documents = [[] for _ in range(num_clusters)]
for doc_index, label in enumerate(labels):
    clustered_documents[label].append((doc_index, documents[doc_index]))

# 找到最接近每个质心的文档索引
def find_closest_docs_to_centroids(embeddings, centroids):
    closest_docs = []
    for centroid in centroids:
        distances = np.linalg.norm(embeddings - centroid, axis=1)
        closest_doc_index = np.argmin(distances)
        closest_docs.append(closest_doc_index)
    return closest_docs

closest_docs = find_closest_docs_to_centroids(document_embeddings, cluster_centers)

# 使用TF-IDF提取代表性单词
vectorizer = TfidfVectorizer()
X = vectorizer.fit_transform(documents)

# 输出每个聚类的文档及其代表性单词，并将索引保存到文件夹
output_dir = "clustered_documents"
os.makedirs(output_dir, exist_ok=True)

for cluster_index, cluster_docs in enumerate(clustered_documents):
    closest_doc_index = closest_docs[cluster_index]
    tfidf_scores = X[closest_doc_index].toarray().flatten()
    top_word_index = np.argmax(tfidf_scores)
    top_word = vectorizer.get_feature_names_out()[top_word_index]
    
    # 创建以代表性单词命名的文件夹
    cluster_dir_name = top_word.replace("/", "_")  # 替换文件名中的不合法字符
    cluster_dir = os.path.join(output_dir, cluster_dir_name)
    os.makedirs(cluster_dir, exist_ok=True)
    
    # 保存文档索引到文件夹
    with open(os.path.join(cluster_dir, "indices.txt"), 'w') as f:
        for doc_index, doc in cluster_docs:
            f.write(f"{doc_index}\n")
    
    # 打印聚类信息和代表性单词
    print(f"Cluster {cluster_index} (Representative word: {top_word}):")
    for doc_index, doc in cluster_docs:
        print(f"  - {doc} (Index: {doc_index})")
    print()

print("Clustering completed. Check the 'clustered_documents' folder for results.")
