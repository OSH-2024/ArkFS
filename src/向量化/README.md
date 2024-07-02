

 ## 1 .向量化检索的构建
 
 pip install  faiss-cpu sentence-transformers


在 Faiss 中，检索结果的距离（distance）表示查询向量与检索结果向量之间的相似度。距离越小，表示两个向量之间的相似度越高，参考example.py

## 2.本地索引库

可以建立一个documents本地文件，(txt)，每一个存入的文件动态的将文件名加入documents中，按行存储，大模型从documents中读取并分析文档关系远近，根据这个远近关系来建立文件树存储。

## 3.聚合

将document内容进行聚合，比如我现在有100个文档，我想将他们放入5个文件夹，我需要将他们关键词提取出来进行聚合、

参考example.py and cluster.py 在使用第二个之前pip install scikit-learn

## 4.新文件夹

将聚合类找到后，我考虑以Representative word为名字，建立文件夹，将文件索引放进去，这样来实现一个简单的文件聚合存储功能。下面需要的就是系统层面，将index转换为系统文件指针，真的将文件存入到新建的文件夹中而不是一个索引。

这部分功能在new_folder里实现。

