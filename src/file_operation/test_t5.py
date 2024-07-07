from transformers import T5Tokenizer, T5ForConditionalGeneration
import torch


def summarize_long_text(long_text, tokenizer, model, max_chunk_length=512, max_summary_length=150, min_summary_length=80):
    # 分割文本成段落
    segments = split_text_into_segments(long_text, max_chunk_length)

    # 初始化结果列表
    summaries = []

    # 处理每个段落
    for segment in segments:
        # 拼接 "summarize " 前缀
        segment = "summarize " + segment

        # 编码和填充输入
        input_ids = tokenizer.encode(segment, return_tensors="pt", max_length=max_chunk_length, truncation=True)

        # 生成摘要
        summary_ids = model.generate(input_ids.to(device), 
                                     max_length=max_summary_length, 
                                     min_length=min_summary_length, 
                                     length_penalty=2.0, 
                                     num_beams=4, 
                                     early_stopping=True)

        # 解码摘要并添加到结果列表
        summary = tokenizer.decode(summary_ids[0], skip_special_tokens=True)
        summaries.append(summary)

    # 返回所有摘要的列表
    return "\n".join(summaries)

def split_text_into_segments(text, max_chunk_length):
    # 根据最大长度分割文本
    segments = []
    words = text.split()
    current_chunk = ""

    for word in words:
        if len(current_chunk) + len(word) < max_chunk_length:
            current_chunk += " " + word
        else:
            segments.append(current_chunk.strip())
            current_chunk = word

    if current_chunk:
        segments.append(current_chunk.strip())

    return segments

# 加载模型和tokenizer
model_name = 't5-base'
tokenizer = T5Tokenizer.from_pretrained(model_name)
model = T5ForConditionalGeneration.from_pretrained(model_name)
device = 'cuda' if torch.cuda.is_available() else 'cpu'
file_path = "E:\\Codefield\\CODE_C\\Git\\ArkFS\\src\\file_operation\\test.txt"

# 要摘要的长文本
with open(file_path, 'r', encoding='utf-8') as f:
                long_text = f.read().strip()

# 生成整体摘要
full_summary = summarize_long_text(long_text, tokenizer, model)

# 打印整体摘要
print("Full Summary:")
print(full_summary)
