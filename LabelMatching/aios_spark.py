
from openai import OpenAI
import time
import ast
import re
from speak_to_text import recognize_speech_from_mic, map_relative_time_to_iso
from datetime import datetime, timedelta


def convert_string_to_list(input_str):
    # 使用正则表达式找到所有中括号中的内容
    matches = re.findall(r'\[([^\[\]]*)\]', input_str)
    return matches

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
        return [[None], [None], [prompt], ['find']]

    if prompt in ["图片", "文本"]:
        return [[None], [prompt], [None], ['find']]

    # Make a request to generate completions based on the model and messages
    completion = client.chat.completions.create(
        model='generalv3.5',  # Specify the model version
        messages=[
            {
                "role": "user",
                "content": (
                    f'"{prompt}",对于这句话请提取他的“时间(昨天、前天或其他)”“文件类型(仅包含image或者txt)”“有关文件内容的一个名词(阳光、草地或人名等其他名词)”，如果有缺失的信息，用NULL表示。现在你有“增、删、改、查”四种文件功能(对于任务调度你只能返回“增、删、改、查”这四个字的组合作为任务序列)，请你给出这句话对应的任务调度序列，如“增删”这样的序列，如果不涉及具体动作，只查即可，但如果有“移动”“转移”“放置”之类的要求，你就需要添加增删改查的其他功能。按照顺序，以[[时间],[文件类型],[内容名词],[调度序列]]的格式返回给我,请改成。'
                )
            }
        ]
    )

     # Extract and format response
    response = completion.choices[0].message.content
    result_list = convert_string_to_list(response)
    return result_list

def get_value(user_input):
    
    try:
        extracted_info = process_input(user_input)
        #print(extracted_info)
        
        if extracted_info == ['None', 'None', 'None','None']:
            #print("输入有误，请重新输入。")
            return None
        else: 
            #print(f"提取的信息: {extracted_info}")
            return extracted_info
    except Exception as e:
        #print(f"发生错误: {e}")
        return None
        
def standard(user_input):
    extracted_=get_value(user_input)
    valid_words = ['增', '删', '改', '查']  # 有效的词语列表
    #print(extracted_)
    while len(extracted_) != 4:
        extracted_=get_value(user_input)

    extracted_[0] = map_relative_time_to_iso(extracted_[0])

    #if '查' not in extracted_[3]:
    #    extracted_[3] = '查' + extracted_[3]

    #if extracted_[3] == '改':

    # 检查第四个参数是否只包含有效的词语
    if all(word in valid_words for word in extracted_[3]):
        pass
    else:
        if '查删增' in extracted_[3]:
            extracted_[3] = '查增删'
        elif  '剪切' in extracted_[3]:
            extracted_[3] = '查增删'
        elif '复制' in extracted_[3]:
            extracted_[3] = '查增'
        elif '移动' in extracted_[3]:
            extracted_[3] = '查增删'

    extracted_[3]=parse_operations(extracted_[3])
        
    if extracted_[1] == 'NULL' and extracted_[2] == 'NULL' and extracted_[3][0] == '3'  and extracted_[0]==('NULL', 'NULL') :
        extracted_[2] = user_input
    
    extracted_[2] = [extracted_[2], ""]
    return extracted_

def parse_operations(param):
    # 可能包含的操作符号映射
    operation_mapping = {
        '增': '0',
        '删': '1',
        '改': '3',
        '查': '3',
        '细': '4'
    }
    
    # 提取参数中的操作符号，并按照出现顺序组成数字序列
    result = []
    for char in param:
        if char in operation_mapping:
            result.append(operation_mapping[char])
    
    result_str = ''.join(result)
    return result_str

#####精确搜索，正则表达式匹配
def is_precise_search(prompt):
    """
    Determine if the search is a precise search based on the input prompt.

    Parameters:
        prompt (str): User input prompt.

    Returns:
        tuple: A boolean indicating if it is a precise search, and the extracted file name.
    """
    precise_patterns = [r'叫(.*?)的文件', r'名为(.*?)的文件']
    for pattern in precise_patterns:
        match = re.search(pattern, prompt)
        if match:
            return True, match.group(1).strip()
    return False, None

def input_user():
    print("请输入一个描述图片信息的句子，例如：“请给我一张昨天修改的带草的图片”。输入'退出'以结束程序。精确化搜索请使用“叫xxx的文件”或“名为xxx的文件”格式。")
    
    user_input=recognize_speech_from_mic()

    is_precise, file_name = is_precise_search(user_input)
    if is_precise:
        print("精确搜索确认")
        print(f"提取的信息: [['NULL'], ['NULL'], [{file_name}," "], ['4']]")
        return [['NULL'], ['NULL'], [file_name,""], ['4']]

    
    if user_input.strip().lower() == '退出':
        print("程序结束。")

    get_v=standard(user_input)

    if(get_v!=None):
        print(f"提取的信息: {get_v}")
        return get_v
    else:
        input_user()


input_user()