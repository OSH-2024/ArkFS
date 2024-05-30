import os
from sentence_transformers import SentenceTransformer
from sklearn.cluster import KMeans
from sklearn.feature_extraction.text import TfidfVectorizer
import numpy as np

import warnings    #消除未知的警报
warnings.filterwarnings("ignore", category=FutureWarning)


# 读取文本文件中的数据
def read_documents(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        documents = file.readlines()
    return [doc.strip() for doc in documents]

# 将文档保存回文件
def save_documents(file_path, documents):
    with open(file_path, 'w', encoding='utf-8') as file:
        for doc in documents:
            file.write(doc + '\n')

# 初始聚类函数
def initial_clustering(documents, num_clusters):
    embedding_model = SentenceTransformer('all-MiniLM-L6-v2')
    document_embeddings = embedding_model.encode(documents)

    kmeans = KMeans(n_clusters=num_clusters, random_state=0)
    kmeans.fit(document_embeddings)

    labels = kmeans.labels_
    cluster_centers = kmeans.cluster_centers_

    clustered_documents = [[] for _ in range(num_clusters)]
    for doc_index, label in enumerate(labels):
        clustered_documents[label].append((doc_index, documents[doc_index]))

    return embedding_model, document_embeddings, kmeans, clustered_documents, cluster_centers

# 更新聚类函数
def update_clustering(documents, embedding_model, kmeans, cluster_centers):
    document_embeddings = embedding_model.encode(documents)
    kmeans.fit(document_embeddings)
    labels = kmeans.labels_
    cluster_centers = kmeans.cluster_centers_

    num_clusters = kmeans.n_clusters
    clustered_documents = [[] for _ in range(num_clusters)]
    for doc_index, label in enumerate(labels):
        clustered_documents[label].append((doc_index, documents[doc_index]))

    return document_embeddings, kmeans, clustered_documents, cluster_centers

# 找到最接近每个质心的文档索引
def find_closest_docs_to_centroids(embeddings, centroids):
    closest_docs = []
    for centroid in centroids:
        distances = np.linalg.norm(embeddings - centroid, axis=1)
        closest_doc_index = np.argmin(distances)
        closest_docs.append(closest_doc_index)
    return closest_docs

# 打印聚类结果并保存索引
def print_and_save_clusters(clustered_documents, closest_docs, documents, X, output_dir):
    vectorizer = TfidfVectorizer()
    X = vectorizer.fit_transform(documents)
    
    os.makedirs(output_dir, exist_ok=True)

    for cluster_index, cluster_docs in enumerate(clustered_documents):
        closest_doc_index = closest_docs[cluster_index]
        tfidf_scores = X[closest_doc_index].toarray().flatten()
        top_word_index = np.argmax(tfidf_scores)
        top_word = vectorizer.get_feature_names_out()[top_word_index]

        cluster_dir_name = top_word.replace("/", "_")
        cluster_dir = os.path.join(output_dir, cluster_dir_name)
        os.makedirs(cluster_dir, exist_ok=True)

        with open(os.path.join(cluster_dir, "indices.txt"), 'w') as f:
            for doc_index, doc in cluster_docs:
                f.write(f"{doc_index}\n")

        print(f"Cluster {cluster_index} (Representative word: {top_word}):")
        for doc_index, doc in cluster_docs:
            print(f"  - {doc} (Index: {doc_index})")
        print()

# 查看聚类结果
def view_clusters(clustered_documents, documents):
    for cluster_index, cluster_docs in enumerate(clustered_documents):
        print(f"Cluster {cluster_index}:")
        for doc_index, doc in cluster_docs:
            print(f"  - {doc} (Index: {doc_index})")
        print()

# 主函数
def main():
    file_path = 'documents.txt'
    documents = read_documents(file_path)
    num_clusters = 5  # 初始聚类数量

    embedding_model, document_embeddings, kmeans, clustered_documents, cluster_centers = initial_clustering(documents, num_clusters)
    closest_docs = find_closest_docs_to_centroids(document_embeddings, cluster_centers)
    print_and_save_clusters(clustered_documents, closest_docs, documents, None, "clustered_documents")

    while True:
        command = input("Enter command (add/del/upd/view/exit): ").strip().lower()

        if command == "add":   ##添加文档
            new_doc = input("Enter new document: ").strip()
            documents.append(new_doc)
            save_documents(file_path, documents)
            document_embeddings, kmeans, clustered_documents, cluster_centers = update_clustering(documents, embedding_model, kmeans, cluster_centers)
            closest_docs = find_closest_docs_to_centroids(document_embeddings, cluster_centers)
            print_and_save_clusters(clustered_documents, closest_docs, documents, None, "clustered_documents")
        
        elif command == "del":  ##删除文档
            try:
                del_index = int(input("Enter index of document to delete: ").strip())
                if 0 <= del_index < len(documents):
                    documents.pop(del_index)
                    save_documents(file_path, documents)
                    document_embeddings, kmeans, clustered_documents, cluster_centers = update_clustering(documents, embedding_model, kmeans, cluster_centers)
                    closest_docs = find_closest_docs_to_centroids(document_embeddings, cluster_centers)
                    print_and_save_clusters(clustered_documents, closest_docs, documents, None, "clustered_documents")
                else:
                    print("Invalid index.")
            except ValueError:
                print("Please enter a valid index.")

        elif command == "upd": ##更新文档，目前只写到文件注册表的更新
            try:
                upd_index = int(input("Enter index of document to update: ").strip())
                if 0 <= upd_index < len(documents):
                    new_content = input("Enter new content: ").strip()
                    documents[upd_index] = new_content
                    save_documents(file_path, documents)
                    document_embeddings, kmeans, clustered_documents, cluster_centers = update_clustering(documents, embedding_model, kmeans, cluster_centers)
                    closest_docs = find_closest_docs_to_centroids(document_embeddings, cluster_centers)
                    print_and_save_clusters(clustered_documents, closest_docs, documents, None, "clustered_documents")
                else:
                    print("Invalid index.")
            except ValueError:
                print("Please enter a valid index.")

        elif command == "view": ##查看文件注册表中的文档
            view_clusters(clustered_documents, documents)

        elif command == "exit":
            break

        else:
            print("Unknown command. Please enter add/del/upd/view/exit.")

if __name__ == "__main__":
    main()
