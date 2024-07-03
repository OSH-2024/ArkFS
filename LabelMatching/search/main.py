from test_deberta import my_search

if __name__ == "__main__":
    modified_time_range = ["2024-07-02T00:00:00", None]
    query_content = "EQ"
    target_folder = "E:\\Codefield\\CODE_C\\Git\\ArkFS\\LabelMatching\\target_folder"

    image_results, text_results = my_search(modified_time_range, query_content, target_folder)
    print("Image Results:", image_results)
    print("Text Results:", text_results)
