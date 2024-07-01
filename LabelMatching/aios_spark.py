
from openai import OpenAI
import time
import ast

client = OpenAI(
				# 控制台获取key和secret拼接，假使APIKey是key123456，APISecret是secret123456
        api_key="6a52536fbbf5c55bdb55cd1daddce81c:NjZhMjM1MDI3YzMwZjgxOGE2ZWY3NTQ5", 
        base_url = 'https://spark-api-open.xf-yun.com/v1' # 指向讯飞星火的请求地址
    )
def process_input(prompt):
    """
    Process user input to extract time, file type, and content keywords.

    Parameters:
        prompt (str): User input prompt.

    Returns:
        list: Nested list containing time, file type, and content keywords.
    """
    # Special cases for single-character input and specific keywords
    if len(prompt) == 1:
        return [[None], [None], [prompt]]

    if prompt in ["图片", "文本"]:
        return [[None], [prompt], [None]]

    # Make a request to generate completions based on the model and messages
    completion = client.chat.completions.create(
        model='generalv3.5',  # Specify the model version
        messages=[
            {
                "role": "user",
                "content": (
                    f'"{prompt}",对于这句话请提取他的“时间(昨天、前天或其他)”'
                    '“文件类型(仅包含image或者txt)”“有关文件内容的一个名词(阳光、草地或其他)”，'
                    '按照顺序，以[[...],[...],[...]]的格式返回给我，如果有缺失的信息，用NULL表示，不要返回其他内容。请输出英文'
                )
            }
        ]
    )

     # Extract and format response
    response = completion.choices[0].message.content
    response_list = [item.strip().strip('"') for item in response.strip('[]').split(',')]
    if response_list[0] == 'None' or response_list[0] == 'none':
        response_list[0] = 'NULL'
    if response_list[1] == 'None' or response_list[1] == 'none':
        response_list[1] = 'NULL'
    if response_list[2] == 'None' or response_list[2] == 'none':
        response_list[2] = 'NULL'
    if response_list[1] == 'Image':
        response_list[0] = 'image'
    return response_list

def main():
    print("请输入一个描述图片信息的句子，例如：“请给我一张昨天修改的带草的图片”。输入'退出'以结束程序。")
    
    while True:
        user_input = input("请输入: ")
        
        if user_input.strip().lower() == '退出':
            print("程序结束。")
            break
        
        try:
            extracted_info = process_input(user_input)
            if extracted_info == [[None], [None], [None]]:
                print("输入有误，请重新输入。")
            else:
                print(f"提取的信息: {extracted_info}")
        except Exception as e:
            print(f"发生错误: {e}")

if __name__ == "__main__":
    main()