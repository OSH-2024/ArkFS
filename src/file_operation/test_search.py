from file_search import my_search
import time

start_time = time.time()

# 定义搜索参数
modified_time = [None, None]  # 示例时间范围
content = "grass"  # 搜索查询文本
target_folder = "E:\\Codefield\\CODE_C\\Git\\ArkFS\\test_directory"  # 目标目录

# 执行搜索
results = my_search([modified_time, content, target_folder])
image_results, text_results = results[0], results[1]

print("图像结果:", image_results)
print("文本结果:", text_results)

end_time = time.time()

print("搜索耗时:", end_time - start_time, "秒")