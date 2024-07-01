import google.generativeai as genai
import os

# Ensure you have set your API key in the environment variables
genai.configure(api_key="AIzaSyA5kauqg6pfL2vmK6p4zz-FJdxqmzzMKUM")

# Initialize the generative model
model = genai.GenerativeModel('gemini-1.5-flash')

def extract_info(prompt):
    """
    Extracts the time, file type, and a keyword related to the file content from a user input prompt.
    
    Parameters:
        prompt (str): The user input prompt.
        
    Returns:
        list: A nested list containing the extracted information.
    """
    # Special cases for single-character input and specific keywords
    if len(prompt) == 1:
        return f"[[NULL], [NULL], [{prompt}]]"
    
    if prompt in ["图片", "文本"]:
        return f"[[NULL], [{prompt}], [NULL]]"
    
    response = model.generate_content(
        f"{prompt}，对于这句话请提取他的“时间(昨天、前天或其他)”“文件类型(只包含图片或者文本)”“有关文件内容的一个名词(阳光、草地或其他)”，按照顺序，以[[...],[...],[...]]的格式返回给我，如果有缺失的信息，用NULL表示，不要返回其他内容。"
    )
    return response.text

# Main function to run the interactive prompt extraction
def main():
    print("请输入一个描述图片信息的句子，例如：“请给我一张昨天修改的带草的图片”。输入'退出'以结束程序。")
    
    while True:
        user_input = input("请输入: ")
        if user_input.strip().lower() == '退出':
            break
        
        try:
            extracted_info = extract_info(user_input)
            print(f"提取的信息: {extracted_info}")
        except Exception as e:
            print(f"发生错误: {e}")

# Run the main function
if __name__ == "__main__":
    main()
