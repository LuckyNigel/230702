import tkinter as tk
import pyautogui
import time
import threading

# 设置点击的坐标
x = 100
y = 200

# 创建启动程序的函数
def start_program():
    global running
    running = True

# 创建停止程序的函数
def stop_program():
    global running
    running = False

# 创建运行程序的函数
def run_program():  
    while running:
        # 获取当前鼠标位置
        current_x, current_y = pyautogui.position()

        # 如果鼠标位置与目标位置不一致，则移动鼠标到目标位置
        if current_x != x or current_y != y:
            pyautogui.moveTo(x, y)
        # 在这里添加缩进的代码块

# 创建一个新线程来运行程序
thread = threading.Thread(target=run_program)

# 点击鼠标
pyautogui.click()

# 等待一段时间
time.sleep(5)

# 创建主窗口
window = tk.Tk()
window.title("鼠标点击程序")
window.geometry("300x200")

# 创建按钮的框架
button_frame = tk.Frame(window)
button_frame.pack(pady=20)

# 创建启动按钮
start_button = tk.Button(button_frame, text="启动", command=start_program)
start_button.pack(side=tk.LEFT, padx=10)

# 创建停止按钮
stop_button = tk.Button(button_frame, text="停止", command=stop_program)
stop_button.pack(side=tk.LEFT, padx=10)

# 设置初始运行状态
running = False

# 开始主事件循环
window.mainloop()