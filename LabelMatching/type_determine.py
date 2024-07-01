import torch
import os
from transformers import XLMRobertaTokenizer, XLMRobertaModel

# 设置环境变量以允许重复的 OpenMP 库
os.environ["KMP_DUPLICATE_LIB_OK"] = "TRUE"

device = "cuda" if torch.cuda.is_available() else "cpu"

# 加载 XLM-R 模型和分词器（用于文本处理）
model_name = "xlm-roberta-base"
tokenizer = XLMRobertaTokenizer.from_pretrained(model_name)
xlm_model = XLMRobertaModel.from_pretrained(model_name).to(device=device)

def classify_query_type(query):
    # Tokenize the query and prepare inputs for XLM-R model
    inputs = tokenizer(query, return_tensors="pt", max_length=512, truncation=True, padding=True)
    
    # Pass inputs through XLM-R model
    with torch.no_grad():
        outputs = xlm_model(**inputs)
    
    # Get the hidden states of all tokens
    hidden_states = outputs.last_hidden_state  # shape: [1, seq_length, hidden_size]
    
    # Consider the mean or max over all tokens
    pooled_output = hidden_states.mean(dim=1)  # Mean pooling over tokens
    
    # Extract logits for each class
    logits = pooled_output[0]
    
    # Determine the type based on the highest logit
    max_logit, max_idx = torch.max(logits, dim=0)
    
    if max_idx == 0:
        return "image"
    elif max_idx == 1:
        return "text"
    elif max_idx == 2:
        return "video"
    else:
        return "unknown"

    
while True:
    query = input("输入查询语句（或输入 'exit' 退出）: ")
    if query.lower() == 'exit':
        break
    
    # 判断文件类型
    file_type = classify_query_type(query)
    print(f"查询类型: {file_type}")
