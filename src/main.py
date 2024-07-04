import tkinter as tk
from tkinter import filedialog
from PIL import Image, ImageTk
import os  # 导入os模块
import query_processing.aios_spark as aios
import file_operation.task_queue as task_queue
import speech_recognition as sr
selected_files = []
sel_filelist = []
confirm_button = None  # Global variable to store the confirm button

# Clear all contents in the UI
def clear():
    global confirm_button
    for widget in result_frame.winfo_children():
        widget.grid_forget()
        widget.destroy()
    if confirm_button:
        confirm_button.pack_forget()  # Hide the confirm button
        confirm_button = None
    update_scroll_region()

# Display content on the UI
def display(content):
    # Calculate the row to add the new content
    current_row = len(result_frame.grid_slaves(column=0))  # Get the current number of rows
    content_label = tk.Label(result_frame, text=str(content), anchor='w', justify='left')
    content_label.grid(row=current_row, column=0, padx=10, pady=10, sticky='w')
    update_scroll_region()

# Define search functionality
def search():
    global sel_filelist
    user_input = search_entry.get()
    clear()
    #display("请输入一个描述图片信息的句子，例如：“请给我一张昨天修改的带草的图片”。")
    #display("精确化搜索请使用“叫xxx的文件”或“名为xxx的文件”格式。")
    #start Li Daifeng
    is_precise, file_name = aios.is_precise_search(user_input)
    if is_precise:
        display("精确搜索确认")
        #print(f"提取的信息: [['NULL'], ['NULL'], [{file_name}," "], ['4']]")
        get_v = [['NULL'], 'NULL', [file_name,""], '4']
    else:
        get_v=aios.standard(user_input)
        
    #end Li Daifeng
    print(get_v)
    #start Yang Bingquan
    if (get_v[3][0] == '3' or get_v[3][0] == '4') and len(get_v[3]) == 1:
        print("select 1")
        tqueue = task_queue.task_queue(get_v)
        filelist = tqueue.execute()
        print(filelist)
        clear()
        input_paths(filelist, 0)
    elif get_v[3][0] == '3':
        print("select 2")
        get_v1 = get_v.copy()
        get_v2 = get_v.copy()
        get_v1[3] = "3"
        get_v2[3] = get_v[3][1:]
        tqueue = task_queue.task_queue(get_v)
        filelist = tqueue.execute()
        clear()
        input_paths(filelist, 1)
        root.wait_variable(decision_made)
        if decision_made.get() == "go":
            clear()
            decision_made.set("")
        get_v2[2][0] = sel_filelist
        tqueue1 = task_queue.task_queue(get_v2)
        state = tqueue1.execute()
        if state == 0:
            display("已完成")
        else:
            display("出错！请重试")
        sel_filelist.clear()
    else:
        tqueue = task_queue.task_queue(get_v)
        filelist = tqueue.execute()
        clear()
        if filelist == 0:
            display("已完成")
        else:
            display("出错！请重试")


    #end Yang Bingquan
    # Add actual search logic here

def recognize_speech_from_mic():
    # 获取默认的麦克风
    recognizer = sr.Recognizer()
    microphone = sr.Microphone()

    # 从麦克风录音
    with microphone as source:
        clear()
        display("请说话...")
        recognizer.adjust_for_ambient_noise(source)
        audio = recognizer.listen(source)

    # 使用 Google Web Speech API 将音频转换为文本
    try:
        display("识别中...")
        text = recognizer.recognize_google(audio, language='zh-CN')
    except sr.UnknownValueError:
        display("Speech无法理解音频")
    except sr.RequestError as e:
        display("无法请求 Google Web Speech API; {0}".format(e))
        

    # 将文本转换为字符串
   # text_str = str(text)

#    # 检查是否包含“手动”
#    if "手动" in text_str:
#        text = input("请输入:")
#    else:
#        print(f"输入结果: {text_str}")
#
    display("识别结束")
    
    return text

def audio_search():
    remove_last_row()
    clear()
    user_input=recognize_speech_from_mic()
    search_entry.delete(0, tk.END)
    search_entry.insert(0,user_input)

    #start Li Daifeng
    #is_precise, file_name = aios.is_precise_search(user_input)
    #if is_precise:
    #    display("精确搜索确认")
    #    #print(f"提取的信息: [['NULL'], ['NULL'], [{file_name}," "], ['4']]")
    #    get_v = [['NULL'], ['NULL'], [file_name,""], ['4']]
#
    #get_v=aios.standard(user_input)
    #end Li Daifeng

# Input file paths via terminal
def input_paths(file_paths, type):
    row = len(result_frame.grid_slaves(column=0))  # Get the current number of rows
    for file_path in file_paths:
        display_file(file_path.strip(), row, type)
        row += 1
    update_scroll_region()

# Open the file when its path is clicked
def open_file(event, file_path):
    try:
        os.startfile(file_path)  # For Windows
    except AttributeError:
        try:
            os.system(f'open "{file_path}"')  # For macOS
        except:
            os.system(f'xdg-open "{file_path}"')  # For Linux

# Display file information and thumbnails
def display_file(file_path, row, show_checkbox=0):
    global confirm_button
    if file_path.lower().endswith(('.png', '.jpg', '.jpeg', '.gif', '.bmp')):
        # Display image thumbnail
        try:
            img = Image.open(file_path)
            img.thumbnail((400, 400))  # Set an appropriate size for the thumbnail
            img = ImageTk.PhotoImage(img)
            img_label = tk.Label(result_frame, image=img)
            img_label.image = img  # Keep a reference to the image
            img_label.grid(row=row, column=0, padx=10, pady=10)
        except Exception as e:
            print(f"Unable to open image: {file_path}, Error: {e}")
    
    # Display file path
    path_label = tk.Label(result_frame, text=file_path, anchor='w', justify='left', fg="blue", cursor="hand2")
    path_label.grid(row=row, column=1, padx=10, pady=10, sticky='w')
    path_label.bind("<Button-1>", lambda e, path=file_path: open_file(e, path))

    if show_checkbox:
        var = tk.IntVar()
        checkbox = tk.Checkbutton(result_frame, variable=var)
        checkbox.grid(row=row, column=2, padx=10, pady=10)
        selected_files.append((file_path, var))
        
        if confirm_button is None:
            confirm_button = tk.Button(root, text="Confirm", command=confirm_selection)
            confirm_button.pack(side="bottom", pady=10)

# Update the scroll region
def update_scroll_region():
    result_frame.update_idletasks()
    result_canvas.config(scrollregion=result_canvas.bbox("all"))

# Confirm button functionality
def confirm_selection():
    global sel_filelist
    selected_list = [file_path for file_path, var in selected_files if var.get() == 1]
    sel_filelist = selected_list
    decision_made.set("go")

# Remove the last row of the UI
def remove_last_row():
    children = result_frame.grid_slaves()
    if children:
        last_row = max(child.grid_info()['row'] for child in children)
        for widget in children:
            if widget.grid_info()['row'] == last_row:
                widget.destroy()
    update_scroll_region()

# Create main window
root = tk.Tk()
root.title("File Display Interface")

# Set window size
root.geometry("1000x600")

# Search frame for search box and buttons
search_frame = tk.Frame(root)
search_frame.pack(pady=10, fill='x')

# Search box
search_entry = tk.Entry(search_frame)
search_entry.pack(side='left', fill='x', expand=True, padx=10)

# Search button
search_button = tk.Button(search_frame, text="确认", command=search)
search_button.pack(side='left', padx=10)

# Audio button
audio_button = tk.Button(search_frame, text="语音输入", command=audio_search)
audio_button.pack(side='left', padx=10)

decision_made = tk.StringVar()
# Clear button
#clear_button = tk.Button(search_frame, text="Clear", command=clear)
#clear_button.pack(side='left', padx=10)

# Display button (for testing display function)
#display_button = tk.Button(search_frame, text="Display Content", command=lambda: display("Test Content"))
#display_button.pack(side='left', padx=10)

# Input paths button
#input_paths_button = tk.Button(search_frame, text="Input Paths", command=input_paths)
#input_paths_button.pack(side='left', padx=10)

# Remove last row button
#remove_last_row_button = tk.Button(search_frame, text="Remove Last Row", command=remove_last_row)
#remove_last_row_button.pack(side='left', padx=10)

# Create Canvas and scrollbar
result_canvas = tk.Canvas(root)
result_scrollbar = tk.Scrollbar(root, orient="vertical", command=result_canvas.yview)
result_canvas.configure(yscrollcommand=result_scrollbar.set)

# Create Frame and place it on the Canvas
result_frame = tk.Frame(result_canvas)
result_canvas.create_window((0, 0), window=result_frame, anchor='nw')

# Layout Canvas and scrollbar
result_canvas.pack(side="left", fill="both", expand=True)
result_scrollbar.pack(side="right", fill="y")

# Enable mouse wheel scrolling
def on_mouse_wheel(event):
    result_canvas.yview_scroll(int(-1*(event.delta/120)), "units")

result_canvas.bind("<MouseWheel>", on_mouse_wheel)

root.after(100, lambda: display("请输入一个描述图片信息的句子，例如：“请给我一张昨天修改的带草的图片”。\n精确化搜索请使用“叫xxx的文件”或“名为xxx的文件”格式。"))
# Run main loop
root.mainloop()
