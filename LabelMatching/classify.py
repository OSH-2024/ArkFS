from datasets import Dataset
from transformers import AutoTokenizer, AutoModelForSequenceClassification
from transformers import Trainer, TrainingArguments
import torch

# 示例数据
data = {
    "word": ["昨天", "文本", "有下雨的画面的图片", "刚才", "今天", "以后"],
    "label": ["时间", "类型", "类型", "时间", "时间", "时间"]
}
dataset = Dataset.from_dict(data)

# 标签编码
labels = list(set(data["label"]))
label2id = {label: i for i, label in enumerate(labels)}

def encode_labels(example):
    example["label"] = label2id[example["label"]]
    return example

dataset = dataset.map(encode_labels)

# 加载预训练的模型和tokenizer
model_name = "google-bert/bert-base-chinese"
tokenizer = AutoTokenizer.from_pretrained(model_name)
model = AutoModelForSequenceClassification.from_pretrained(model_name, num_labels=len(labels))

def tokenize_batch(batch):
    return tokenizer(batch["word"], padding="max_length", truncation=True, max_length=16)

# 对数据集进行预处理和编码
encoded_dataset = dataset.map(tokenize_batch, batched=True)

# 定义训练参数
training_args = TrainingArguments(
    output_dir="./results",
    num_train_epochs=100,
    per_device_train_batch_size=16,
    per_device_eval_batch_size=16,
    warmup_steps=500,
    weight_decay=0.01,
    logging_dir="./logs",
)

# 定义Trainer对象并训练模型
trainer = Trainer(
    model=model,
    args=training_args,
    train_dataset=encoded_dataset,
    eval_dataset=encoded_dataset,
)
trainer.train()

# 定义分类函数
def classify_word(word, model, tokenizer):
    inputs = tokenizer(word, return_tensors="pt", padding="max_length", truncation=True, max_length=16)
    outputs = model(**inputs)
    logits = outputs.logits
    predicted_class_id = logits.argmax().item()
    predicted_label = labels[predicted_class_id]
    return predicted_label

# 测试新词汇的分类
new_words = ["带草的图片", "之前"]
for word in new_words:
    predicted_label = classify_word(word, model, tokenizer)
    print(f"Word: {word}, Predicted Label: {predicted_label}")
