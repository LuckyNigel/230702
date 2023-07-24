import tkinter as tk
import threading
import ctypes
import pyautogui
import time
import pyperclip
from pynput.mouse import Listener as MouseListener
from pynput.keyboard import Controller as KeyboardController
from pynput.mouse import Controller as MouseController
from pynput.keyboard import Key, Listener as KeyboardListener

# 定义全局变量坐标
global coord_x1, coord_y1, coord_x2, coord_y2, coord_x3, coord_y3
coord_x1, coord_y1, coord_x2, coord_y2, coord_x3, coord_y3 = 0, 0, 0, 0, 0, 0

keyboard_active = False

def on_key_press(key):
    global keyboard_active
    keyboard_active = True

def on_key_release(key):
    global keyboard_active
    keyboard_active = False

# 在一个新的线程中启动键盘监听器
keyboard_listener = KeyboardListener(on_press=on_key_press, on_release=on_key_release)
keyboard_listener.start()

def on_click(x, y, button, pressed):
    # 当鼠标左键被按下时，更新坐标
    if pressed:
        global coord_x1, coord_y1, coord_x2, coord_y2, coord_x3, coord_y3
        if coord_x1 == coord_y1 == 0:
            coord_x1, coord_y1 = x, y
            coord_label1.config(text="x: {}, y: {}".format(coord_x1, coord_y1), bg="#D8BFD8")
        elif coord_x2 == coord_y2 == 0:
            coord_x2, coord_y2 = x, y
            coord_label2.config(text="x: {}, y: {}".format(coord_x2, coord_y2), bg="#D8BFD8")
        else:
            coord_x3, coord_y3 = x, y
            coord_label3.config(text="x: {}, y: {}".format(coord_x3, coord_y3), bg="#D8BFD8")
            return False  # 停止监听

def copy_coord():
    # 启动鼠标监听
    listener = MouseListener(on_click=on_click)
    listener.start()  # 使用start而不是join，以便在监听鼠标的同时继续运行其他代码

def start_program():
    # 在新的线程中运行你的程序
    threading.Thread(target=your_program).start()

def stop_program():
    # 停止你的程序
    global end_time
    end_time = time.time()  # 立即结束循环

# 创建键盘和鼠标控制器
keyboard = KeyboardController()
mouse = MouseController()

def your_program():
    # 关闭安全特性
    pyautogui.FAILSAFE = False

    # 延迟5秒启动
    time.sleep(5)

    try:
        # 循环持续10分钟
        global end_time
        end_time = time.time() + 60*60  # 60分钟后的时间
        while time.time() < end_time:
            try:
                # 移动鼠标到指定位置并点击
                global coord_x1, coord_y1, coord_x2, coord_y2, coord_x3, coord_y3
                pyautogui.moveTo(coord_x1, coord_y1)
                pyautogui.click()
                #time.sleep(0)  # 等待0秒

                pyautogui.moveTo(coord_x2, coord_y2)
                pyautogui.click()
                time.sleep(5)  # 等待5秒

                pyautogui.moveTo(coord_x3, coord_y3)
                pyautogui.click()
                time.sleep(1)  # 等待1秒

            except pyautogui.FailSafeException:
                # 在你的代码中检查键盘是否活跃
                while True:
                    time.sleep(5)  # 暂停5秒
                    # 如果鼠标和键盘沉默5秒，则恢复运行
                    if mouse.position == (coord_x, coord_y) and not keyboard_active:
                        break
                    keyboard_active = False  # 重置键盘活动状态
                continue

    except KeyboardInterrupt:
        return(0)

# 创建窗体
root = tk.Tk()

# 设置窗体的名称
root.title("中控助手 by ZZ")

# 设置窗体始终在最前方
root.attributes('-topmost', 1)

# 设置窗体的最小大小
root.minsize(400, 125)

# 创建一个Frame
frame = tk.Frame(root)
frame.place(relx=0.5, rely=0.5, anchor='center')  # 将Frame居中

# 创建一个用于显示坐标的Label
coord_label1 = tk.Label(root, text="x: 0, y: 0", bg="grey")
coord_label1.place(x=0, y=0, anchor='nw')  # 将Label放在窗体的左上角

coord_label2 = tk.Label(root, text="x: 0, y: 0", bg="grey")
coord_label2.place(x=0, y=75, anchor='nw')  # 将Label放在第一个标签的下方，中间间隔75像素

coord_label3 = tk.Label(root, text="x: 0, y: 0", bg="grey")
coord_label3.place(x=0, y=150, anchor='nw')  # 将Label放在第二个标签的下方，中间间隔75像素

# 创建一个Frame
frame = tk.Frame(root)
frame.place(relx=0.75, rely=0.5, anchor='center')  # 将Frame放在窗体的右侧四分之一处

# 创建复制坐标按钮
copy_button = tk.Button(frame, text="选择坐标", command=copy_coord)
copy_button.pack(side=tk.TOP, pady=(50, 10))  # 按钮高度的一半假设为50像素，上下间隔10像素

# 创建开始按钮
start_button = tk.Button(frame, text="开始", command=start_program)
start_button.pack(side=tk.TOP, pady=(10, 10))  # 按钮高度的一半假设为50像素，上下间隔10像素

# 创建停止按钮
stop_button = tk.Button(frame, text="停止", command=stop_program)
stop_button.pack(side=tk.TOP, pady=(10, 50))  # 按钮高度的一半假设为50像素，上下间隔10像素

# 显示窗体
root.mainloop()