import tkinter as tk
from tkinter import filedialog
from PIL import Image, ImageTk

selected_files = []
confirm_button = None  # 全局变量存储确定按钮

# 清除UI上的所有内容
def clear():
    global confirm_button
    for widget in result_frame.winfo_children():
        widget.destroy()
    if confirm_button:
        confirm_button.pack_forget()  # 隐藏确定按钮
        confirm_button = None
    update_scroll_region()

# 在UI上打印参数内容
def display(content):
    # 计算新内容应该添加到哪一行
    current_row = len(result_frame.grid_slaves(column=0))  # 获取当前有多少行
    content_label = tk.Label(result_frame, text=str(content), anchor='w', justify='left')
    content_label.grid(row=current_row, column=0, padx=10, pady=10, sticky='w')
    update_scroll_region()

# 定义搜索功能
def search():
    search_query = search_entry.get()
    print(f"搜索内容: {search_query}")
    # 在此处可以添加实际搜索逻辑
    clear()

# 通过终端输入路径
def input_paths():
    file_paths = input("请输入文件的绝对路径，以逗号分隔: ").split(',')
    row = len(result_frame.grid_slaves(column=0))  # 获取当前有多少行
    for file_path in file_paths:
        display_file(file_path.strip(), row, 1)
        row += 1
    update_scroll_region()

# 显示文件信息和缩略图
def display_file(file_path, row, show_checkbox=0):
    global confirm_button
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

    if show_checkbox:
        var = tk.IntVar()
        checkbox = tk.Checkbutton(result_frame, variable=var)
        checkbox.grid(row=row, column=2, padx=10, pady=10)
        selected_files.append((file_path, var))
        
        if confirm_button is None:
            confirm_button = tk.Button(root, text="确定", command=confirm_selection)
            confirm_button.pack(side="bottom", pady=10)

# 更新滚动区域
def update_scroll_region():
    result_frame.update_idletasks()
    result_canvas.config(scrollregion=result_canvas.bbox("all"))

# 确定按钮功能
def confirm_selection():
    selected_list = [file_path for file_path, var in selected_files if var.get() == 1]
    print("Selected files:", selected_list)

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

# 清除按钮
clear_button = tk.Button(search_frame, text="清除", command=clear)
clear_button.pack(side='left', padx=10)

# 显示按钮（用于测试display函数）
display_button = tk.Button(search_frame, text="显示内容", command=lambda: display("测试内容"))
display_button.pack(side='left', padx=10)

# 输入路径按钮
input_paths_button = tk.Button(search_frame, text="输入路径", command=input_paths)
input_paths_button.pack(side='left', padx=10)

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
root.mainloop()
