import tkinter as tk
from tkinter import filedialog
from PIL import Image, ImageTk

# 定义搜索功能
def search():
    file_paths = filedialog.askopenfilenames()
    for widget in result_frame.winfo_children():
        widget.destroy()
    row = 0
    for file_path in file_paths:
        display_file(file_path, row)
        row += 1
    # 更新canvas scrollregion
    result_frame.update_idletasks()
    result_canvas.config(scrollregion=result_canvas.bbox("all"))

# 显示文件信息和缩略图
def display_file(file_path, row):
    if file_path.lower().endswith(('.png', '.jpg', '.jpeg', '.gif', '.bmp')):
        # 显示图片缩略图
        try:
            img = Image.open(file_path)
            img.thumbnail((400, 400))  # 将缩略图大小设置为原来的4倍
            img = ImageTk.PhotoImage(img)
            img_label = tk.Label(result_frame, image=img)
            img_label.image = img  # 保持对图像的引用
            img_label.grid(row=row, column=0, padx=10, pady=10)
        except Exception as e:
            print(f"无法打开图片: {file_path}, 错误: {e}")
    # 显示文件路径
    path_label = tk.Label(result_frame, text=file_path, anchor='w', justify='left')
    path_label.grid(row=row, column=1, padx=10, pady=10, sticky='w')

# 创建主窗口
root = tk.Tk()
root.title("文件展示界面")

# 设置窗口大小
root.geometry("800x600")

# 搜索框标签
search_label = tk.Label(root, text="点击按钮选择文件：")
search_label.pack(pady=10)

# 搜索按钮
search_button = tk.Button(root, text="搜索", command=search)
search_button.pack(pady=10)

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
