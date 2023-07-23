import tkinter as tk
import threading
import ctypes
import pyautogui
import time
import pyperclip
from pynput.mouse import Listener

# 定义全局变量
global coord_x, coord_y
coord_x, coord_y = 0, 0

def on_click(x, y, button, pressed):
    # 当鼠标左键被按下时，更新坐标
    if pressed:
        global coord_x, coord_y
        coord_x, coord_y = x, y
        # 更新coord_label的文本和背景颜色
        coord_label.config(text="x: {}, y: {}".format(coord_x, coord_y), bg="#D8BFD8")

def copy_coord():
    # 启动鼠标监听
    listener = Listener(on_click=on_click)
    listener.start()  # 使用start而不是join，以便在监听鼠标的同时继续运行其他代码

def start_program():
    # 在新的线程中运行你的程序
    threading.Thread(target=your_program).start()

def stop_program():
    # 停止你的程序
    global end_time
    end_time = time.time()  # 立即结束循环

def your_program():
    # 关闭安全特性
    pyautogui.FAILSAFE = False

    # 延迟5秒启动
    time.sleep(5)

    try:
        # 循环持续10分钟
        global end_time
        end_time = time.time() + 10*60  # 10分钟后的时间
        while time.time() < end_time:
            try:
                # 移动鼠标到指定位置
                global coord_x, coord_y
                pyautogui.moveTo(coord_x, coord_y)

                # 更新coord_label的文本
                coord_label.config(text="x: {}, y: {}".format(coord_x, coord_y))

                # 在当前位置点击鼠标
                pyautogui.click()

                # 等待6秒
                time.sleep(6)

                # 再次点击
                pyautogui.click()

                # 等待2秒
                time.sleep(2)

            except pyautogui.FailSafeException:
                print("检测到鼠标异常,程序将在10秒后重新启动")
                time.sleep(20)
                continue

    except KeyboardInterrupt:
        print("程序被用户手动停止")

# 创建窗体
root = tk.Tk()

# 设置窗体的名称
root.title("中控助手")

# 设置窗体的最小大小
root.minsize(350, 125)

# 创建一个Frame
frame = tk.Frame(root)
frame.place(relx=0.5, rely=0.5, anchor='center')  # 将Frame居中

# 创建一个用于显示坐标的Label
coord_label = tk.Label(root, text="x: 0, y: 0", bg="grey")
coord_label.place(x=0, y=0, anchor='nw')  # 将Label放在窗体的右上角

# 创建复制坐标按钮
copy_button = tk.Button(frame, text="选择坐标", command=copy_coord)
copy_button.pack(side=tk.LEFT, padx=(0, 25))  # 按钮宽度的一半假设为50像素

# 创建开始按钮
start_button = tk.Button(frame, text="开始", command=start_program)
start_button.pack(side=tk.LEFT, padx=(0, 25))  # 按钮宽度的一半假设为50像素

# 创建停止按钮
stop_button = tk.Button(frame, text="停止", command=stop_program)
stop_button.pack(side=tk.LEFT)

# 显示窗体
root.mainloop()