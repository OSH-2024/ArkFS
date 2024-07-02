import tkinter as tk
from tkinter import filedialog
from PIL import Image, ImageTk

# 定义搜索功能
def search():
    search_query = search_entry.get()
    print(f"搜索内容: {search_query}")
    # 在此处可以添加实际搜索逻辑
    for widget in result_frame.winfo_children():
        widget.destroy()

# 通过终端输入路径
def input_paths():
    file_paths = input("请输入文件的绝对路径，以逗号分隔: ").split(',')
    for widget in result_frame.winfo_children():
        widget.destroy()
    row = 0
    for file_path in file_paths:
        display_file(file_path.strip(), row)
        row += 1
    update_scroll_region()

# 显示文件信息和缩略图
def display_file(file_path, row):
    if file_path.lower().endswith(('.png', '.jpg', '.jpeg', '.gif', '.bmp')):
        # 显示图片缩略图
        try:
            img = Image.open(file_path)
            img.thumbnail((400, 400))  # 将缩略图大小设置为合适的大小
            img = ImageTk.PhotoImage(img)
            img_label = tk.Label(result_frame, image=img)
            img_label.image = img  # 保持对图像的引用
            img_label.grid(row=row, column=0, padx=10, pady=10)
        except Exception as e:
            print(f"无法打开图片: {file_path}, 错误: {e}")
    # 显示文件路径
    path_label = tk.Label(result_frame, text=file_path, anchor='w', justify='left')
    path_label.grid(row=row, column=1, padx=10, pady=10, sticky='w')

# 更新滚动区域
def update_scroll_region():
    result_frame.update_idletasks()
    result_canvas.config(scrollregion=result_canvas.bbox("all"))

# 创建主窗口
root = tk.Tk()
root.title("文件展示界面")

# 设置窗口大小
root.geometry("800x600")

# 搜索框和按钮框架
search_frame = tk.Frame(root)
search_frame.pack(pady=10, fill='x')

# 搜索框
search_entry = tk.Entry(search_frame)
search_entry.pack(side='left', fill='x', expand=True, padx=10)

# 搜索按钮
search_button = tk.Button(search_frame, text="搜索", command=search)
search_button.pack(side='left', padx=10)

# 创建Canvas和滚动条
result_canvas = tk.Canvas(root)
result_scrollbar = tk.Scrollbar(root, orient="vertical", command=result_canvas.yview)
result_canvas.configure(yscrollcommand=result_scrollbar.set)

# 创建Frame并放置在Canvas上
result_frame = tk.Frame(result_canvas)
result_canvas.create_window((0, 0), window=result_frame, anchor='nw')

# 布局Canvas和滚动条
result_canvas.pack(side="left", fill="both", expand=True)
result_scrollbar.pack(side="right", fill="y")

# 使Canvas支持鼠标滚轮
def on_mouse_wheel(event):
    result_canvas.yview_scroll(int(-1*(event.delta/120)), "units")

result_canvas.bind("<MouseWheel>", on_mouse_wheel)

# 运行主循环
root.after(100, input_paths)  # 在主循环开始后调用input_paths函数

root.mainloop()
