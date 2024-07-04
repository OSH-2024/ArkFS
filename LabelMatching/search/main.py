from file_search import my_search

if __name__ == "__main__":
    modified_time_range = [None, None]
    query_content = "grass"
    target_folder = "D:\\arkfs\\LabelMatching\\target_folder"

    image_results, text_results = my_search([modified_time_range, query_content, target_folder])
    print("Image Results:", image_results)
    print("Text Results:", text_results)
