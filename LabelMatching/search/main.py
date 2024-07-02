from file_search import my_search

if __name__ == "__main__":
    modified_time_range = ["2024-07-01T00:00:00", "2024-07-01T23:59:59"]
    query_content = "grass pictures"
    target_folder = "E:\\Codefield\\CODE_C\\Git\\ArkFS\\LabelMatching\\target_folder"

    image_results, text_results = my_search(modified_time_range, query_content, target_folder)
    print("Image Results:", image_results)
    print("Text Results:", text_results)
