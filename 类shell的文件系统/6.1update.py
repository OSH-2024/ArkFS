import os
import shutil
from sentence_transformers import SentenceTransformer
from transformers import pipeline, BlipProcessor, BlipForConditionalGeneration
from sklearn.cluster import KMeans
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.feature_extraction.text import TfidfVectorizer
import numpy as np
import torch
import warnings

warnings.filterwarnings("ignore", category=FutureWarning)

# 使用transformers库中的summarization管道来生成文本摘要
summarizer = pipeline("summarization", model="facebook/bart-large-cnn")

# 使用transformers库中的BLIP模型来生成图像描述
blip_processor = BlipProcessor.from_pretrained("Salesforce/blip-image-captioning-base")
blip_model = BlipForConditionalGeneration.from_pretrained("Salesforce/blip-image-captioning-base")

# 读取目标文件夹中的所有文件内容并生成摘要
def read_and_summarize_documents(folder_path):
    documents = []
    file_paths = []
    for file_name in os.listdir(folder_path):
        file_path = os.path.join(folder_path, file_name)
        if os.path.isfile(file_path):
            if file_name.endswith(('.txt', '.md')):
                with open(file_path, 'r', encoding='utf-8') as file:
                    content = file.read()
                    summary = summarize_text(content)
                    documents.append(summary)
            elif file_name.endswith(('.png', '.jpg', '.jpeg', '.bmp', '.gif')):
                summary = summarize_image(file_path)
                documents.append(summary)
            file_paths.append(file_path)
    return documents, file_paths

# 使用大模型生成文本摘要
def summarize_text(text):
    summarized = summarizer(text, max_length=50, min_length=25, do_sample=False)
    return summarized[0]['summary_text']

# 使用大模型从图片中抽象出内容
def summarize_image(image_path):
    image = blip_processor(images=image_path, return_tensors="pt")
    with torch.no_grad():
        generated_ids = blip_model.generate(**image)
    description = blip_processor.batch_decode(generated_ids, skip_special_tokens=True)[0]
    return description

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

# 计算聚类内的相似度（距离）
def calculate_similarity(embedding1, embedding2):
    return cosine_similarity([embedding1], [embedding2])[0][0]

# 更新聚类函数
def update_clustering(documents, document_embeddings, embedding_model, cluster_centers, clustered_documents, similarity_threshold):
    new_embeddings = embedding_model.encode(documents[-1:])  # 只编码新文档
    new_embedding = new_embeddings[0]
    
    best_cluster = -1
    best_similarity = -1
    for i, centroid in enumerate(cluster_centers):
        similarity = calculate_similarity(new_embedding, centroid)
        if similarity > best_similarity:
            best_similarity = similarity
            best_cluster = i
    
    if best_similarity >= similarity_threshold:
        # 将新文档加入最佳聚类
        clustered_documents[best_cluster].append((len(documents) - 1, documents[-1]))
        # 更新质心
        cluster_indices = [doc_index for doc_index, _ in clustered_documents[best_cluster]]
        cluster_embeddings = document_embeddings[cluster_indices + [len(documents) - 1]]
        new_centroid = np.mean(cluster_embeddings, axis=0)
        cluster_centers[best_cluster] = new_centroid
    else:
        # 创建新的聚类
        cluster_centers = np.vstack([cluster_centers, new_embedding])
        clustered_documents.append([(len(documents) - 1, documents[-1])])
    
    return document_embeddings, cluster_centers, clustered_documents

# 找到最接近每个质心的文档索引
def find_closest_docs_to_centroids(embeddings, centroids):
    closest_docs = []
    for centroid in centroids:
        distances = np.linalg.norm(embeddings - centroid, axis=1)
        closest_doc_index = np.argmin(distances)
        closest_docs.append(closest_doc_index)
    return closest_docs

# 打印聚类结果并保存索引
def print_and_save_clusters(clustered_documents, closest_docs, documents, file_paths, output_dir):
    vectorizer = TfidfVectorizer()
    X = vectorizer.fit_transform(documents)
    
    if os.path.exists(output_dir):
        shutil.rmtree(output_dir)
    os.makedirs(output_dir, exist_ok=True)

    for cluster_index, cluster_docs in enumerate(clustered_documents):
        closest_doc_index = closest_docs[cluster_index]
        tfidf_scores = X[closest_doc_index].toarray().flatten()
        top_word_indices = np.argsort(tfidf_scores)[-3:][::-1]  # 取分数最高的三个词
        top_words = [vectorizer.get_feature_names_out()[index] for index in top_word_indices]

        cluster_dir_name = "_".join([word.replace("/", "_") for word in top_words])
        cluster_dir = os.path.join(output_dir, cluster_dir_name)
        os.makedirs(cluster_dir, exist_ok=True)

        with open(os.path.join(cluster_dir, "indices.txt"), 'w') as f:
            for doc_index, _ in cluster_docs:
                f.write(f"{doc_index}\n")
                # 复制文件到相应的聚类文件夹
                shutil.copy(file_paths[doc_index], cluster_dir)

        print(f"Cluster {cluster_index} (Representative words: {', '.join(top_words)}):")
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
    folder_path = 'target_folder'  # 目标文件夹路径
    output_dir = 'clustered_documents'  # 输出文件夹路径
    documents_file = 'documents.txt'  # 存储摘要的文档文件

    documents, file_paths = read_and_summarize_documents(folder_path)
    save_documents(documents_file, documents)  # 保存摘要到文档文件
    num_clusters = 5  # 初始聚类数量
    similarity_threshold = 0.4  # 相似度阈值

    embedding_model, document_embeddings, kmeans, clustered_documents, cluster_centers = initial_clustering(documents, num_clusters)
    closest_docs = find_closest_docs_to_centroids(document_embeddings, cluster_centers)
    print_and_save_clusters(clustered_documents, closest_docs, documents, file_paths, output_dir)

    while True:
        command = input("Enter command (add/del/upd/view/exit): ").strip().lower()

        if command == "add":
            new_doc_path = input("Enter path to new document: ").strip()
            if os.path.isfile(new_doc_path):
                if new_doc_path.endswith(('.txt', '.md')):
                    with open(new_doc_path, 'r', encoding='utf-8') as file:
                        new_doc_content = file.read()
                        new_doc_summary = summarize_text(new_doc_content)
                elif new_doc_path.endswith(('.png', '.jpg', '.jpeg', '.bmp', '.gif')):
                    new_doc_summary = summarize_image(new_doc_path)
                documents.append(new_doc_summary)
                file_paths.append(new_doc_path)
                save_documents(documents_file, documents)  # 保存摘要到文档文件

                document_embeddings = np.vstack([document_embeddings, embedding_model.encode([new_doc_summary])])
                document_embeddings, cluster_centers, clustered_documents = update_clustering(documents, document_embeddings, embedding_model, cluster_centers, clustered_documents, similarity_threshold)
                closest_docs = find_closest_docs_to_centroids(document_embeddings, cluster_centers)
                print_and_save_clusters(clustered_documents, closest_docs, documents, file_paths, output_dir)
        
        elif command == "del":
            try:
                del_index = int(input("Enter index of document to delete: ").strip())
                if 0 <= del_index < len(documents):
                    documents.pop(del_index)
                    file_paths.pop(del_index)
                    save_documents(documents_file, documents)  # 保存摘要到文档文件

                    # 重新聚类
                    num_clusters = len(clustered_documents)
                    embedding_model, document_embeddings, kmeans, clustered_documents, cluster_centers = initial_clustering(documents, num_clusters)
                    closest_docs = find_closest_docs_to_centroids(document_embeddings, cluster_centers)
                    print_and_save_clusters(clustered_documents, closest_docs, documents, file_paths, output_dir)
                else:
                    print("Invalid index.")
            except ValueError:
                print("Please enter a valid index.")

        elif command == "upd":
            try:
                upd_index = int(input("Enter index of document to update: ").strip())
                if 0 <= upd_index < len(documents):
                    new_doc_path = input("Enter path to new document: ").strip()
                    if os.path.isfile(new_doc_path):
                        if new_doc_path.endswith(('.txt', '.md')):
                            with open(new_doc_path, 'r', encoding='utf-8') as file:
                                new_doc_content = file.read()
                                new_doc_summary = summarize_text(new_doc_content)
                        elif new_doc_path.endswith(('.png', '.jpg', '.jpeg', '.bmp', '.gif')):
                            new_doc_summary = summarize_image(new_doc_path)
                        documents[upd_index] = new_doc_summary
                        file_paths[upd_index] = new_doc_path
                        save_documents(documents_file, documents)  # 保存摘要到文档文件

                        # 重新聚类
                        num_clusters = len(clustered_documents)
                        embedding_model, document_embeddings, kmeans, clustered_documents, cluster_centers = initial_clustering(documents, num_clusters)
                        closest_docs = find_closest_docs_to_centroids(document_embeddings, cluster_centers)
                        print_and_save_clusters(clustered_documents, closest_docs, documents, file_paths, output_dir)
                else:
                    print("Invalid index.")
            except ValueError:
                print("Please enter a valid index.")

        elif command == "view":
            view_clusters(clustered_documents, documents)

        elif command == "exit":
            break

        else:
            print("Unknown command. Please enter 'add', 'del', 'upd', 'view', or 'exit'.")

if __name__ == "__main__":
    main()
