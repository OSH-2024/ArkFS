# 导入SDK，发起请求
from openai import OpenAI
client = OpenAI(
				# 控制台获取key和secret拼接，假使APIKey是key123456，APISecret是secret123456
        api_key="6a52536fbbf5c55bdb55cd1daddce81c:NjZhMjM1MDI3YzMwZjgxOGE2ZWY3NTQ5", 
        base_url = 'https://spark-api-open.xf-yun.com/v1' # 指向讯飞星火的请求地址
    )
completion = client.chat.completions.create(
    model='generalv3.5', # 指定请求的版本
    messages=[
        {
            "role": "user",
            "content":' "我需要一张带草地的图片"，对于这句话请提取他的“时间(昨天、前天或其他)”'
                    '“文件类型(只包含图片或者文本)”“有关文件内容的一个名词(阳光、草地或其他)”，'
                    '按照顺序，以[[...],[...],[...]]的格式返回给我，如果有缺失的信息，用NULL表示，不要返回其他内容。请输出英文,格式为python的列表'
        }
    ]
)
print(completion.choices[0].message.content)
print(type(completion.choices[0].message.content))