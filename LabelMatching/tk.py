import tkinter as tk

def on_first_confirm():
    """
    第一级确认的处理函数。
    """
    # 获取输入框的内容
    input_text = entry.get()
    # 清空输入框
    entry.delete(0, tk.END)
    # 在标签上显示中间消息
    label.config(text="Do you accept or decline?")
    # 禁用第一个确认按钮，启用接收和放弃按钮
    first_confirm_button.config(state=tk.DISABLED)
    accept_button.config(state=tk.NORMAL)
    decline_button.config(state=tk.NORMAL)
    # 阻塞等待，直到接收或放弃按钮被点击
    root.wait_variable(decision_made)
    if decision_made.get() == "accept":
        # 用户选择接收
        label.config(text="You accepted. Hello")
    else:
        # 用户选择放弃
        label.config(text="You declined.")
    # 禁用接收和放弃按钮
    accept_button.config(state=tk.DISABLED)
    decline_button.config(state=tk.DISABLED)

def on_accept():
    """
    接收按钮的处理函数。
    """
    decision_made.set("accept")

def on_decline():
    """
    放弃按钮的处理函数。
    """
    decision_made.set("decline")

# 创建主窗口
root = tk.Tk()
root.title("Blocking Button Example")

# 创建一个输入框
entry = tk.Entry(root, width=40)
entry.pack(pady=10)

# 创建第一级确认按钮，并绑定点击事件
first_confirm_button = tk.Button(root, text="确认第一级", command=on_first_confirm)
first_confirm_button.pack(pady=10)

# 创建一个用于阻塞的变量
decision_made = tk.StringVar()

# 创建接收和放弃按钮，并绑定点击事件，初始时禁用
accept_button = tk.Button(root, text="接收", command=on_accept, state=tk.DISABLED)
accept_button.pack(pady=10)

decline_button = tk.Button(root, text="放弃", command=on_decline, state=tk.DISABLED)
decline_button.pack(pady=10)

# 创建一个标签，用于显示结果
label = tk.Label(root, text="", font=("Helvetica", 14))
label.pack(pady=10)

# 运行主循环
root.mainloop()
