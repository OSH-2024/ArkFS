import faiss
from sentence_transformers import SentenceTransformer

# 示例文本数据
documents = [
    "I love programming in Python",
    "Python is a great language",
    "I enjoy learning new things",
    "Machine learning is fascinating",
    "Natural language processing is a part of AI",
    "Python is the best programming language",
    "I love working on new projects",
    "I enjoy coding with Python",
    "I love working with data",
    "I love working with data science",
    "I love working with data science and machine learning",
    "Tell me about Python programming"
]

# 初始化句子嵌入模型
embedding_model = SentenceTransformer('all-MiniLM-L6-v2')

# 生成嵌入
document_embeddings = embedding_model.encode(documents)

# 创建 FAISS 索引
dimension = document_embeddings.shape[1]
faiss_index = faiss.IndexFlatL2(dimension)

# 添加文档嵌入到索引中
faiss_index.add(document_embeddings)

# 查询向量
query_vector = embedding_model.encode(["Tell me about Python programming"])

# 使用 FAISS 进行检索
k = 3  # 返回前 k 个最相似的文档
distances, indices = faiss_index.search(query_vector, k)

# 打印检索结果
print("Top", k, "most similar documents:")
for i, idx in enumerate(indices[0]):
    print("Document:", documents[idx], "- Distance:", distances[0][i])
