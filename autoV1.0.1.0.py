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

# 初始化全局坐标变量
global coord_x1, coord_y1, coord_x2, coord_y2, coord_x3, coord_y3
coord_x1, coord_y1, coord_x2, coord_y2, coord_x3, coord_y3 = 0, 0, 0, 0, 0, 0

keyboard_active = False

# 键盘按下事件处理
def on_key_press(key):
    global keyboard_active
    keyboard_active = True

# 键盘释放事件处理
def on_key_release(key):
    global keyboard_active
    keyboard_active = False

# 启动键盘监听
keyboard_listener = KeyboardListener(on_press=on_key_press, on_release=on_key_release)
keyboard_listener.start()

# 鼠标点击事件处理
def on_click(x, y, button, pressed):
    if pressed:
        global coord_x1, coord_y1, coord_x2, coord_y2, coord_x3, coord_y3
        # 记录第一次点击的坐标
        if coord_x1 == coord_y1 == 0:
            coord_x1, coord_y1 = x, y
            coord_label1.config(text="x: {}, y: {}".format(coord_x1, coord_y1), bg="#D8BFD8")
        # 记录第二次点击的坐标
        elif coord_x2 == coord_y2 == 0:
            coord_x2, coord_y2 = x, y
            coord_label2.config(text="x: {}, y: {}".format(coord_x2, coord_y2), bg="#D8BFD8")
        # 记录第三次点击的坐标
        else:
            coord_x3, coord_y3 = x, y
            coord_label3.config(text="x: {}, y: {}".format(coord_x3, coord_y3), bg="#D8BFD8")
            return False  

# 启动鼠标监听
def copy_coord():
    listener = MouseListener(on_click=on_click)
    listener.start()  

# 启动程序
def start_program():
    threading.Thread(target=your_program).start()

# 停止程序
def stop_program():
    global end_time
    end_time = time.time()  

keyboard = KeyboardController()
mouse = MouseController()

# 主程序
def your_program():
    pyautogui.FAILSAFE = False

    time.sleep(5)

    try:
        global end_time
        end_time = time.time() + 240*60  
        while time.time() < end_time:
            try:
                global coord_x1, coord_y1, coord_x2, coord_y2, coord_x3, coord_y3
                # 移动到第一次点击的坐标并点击
                pyautogui.moveTo(coord_x1, coord_y1)
                pyautogui.click()

                # 移动到第二次点击的坐标并点击
                pyautogui.moveTo(coord_x2, coord_y2)
                pyautogui.click()
                time.sleep(5)  

                # 移动到第三次点击的坐标并点击
                pyautogui.moveTo(coord_x3, coord_y3)
                pyautogui.click()
                time.sleep(1)  

            except pyautogui.FailSafeException:
                while True:
                    time.sleep(5)  
                    if mouse.position == (coord_x1, coord_y1) and not keyboard_active:
                        break
                    keyboard_active = False  
                continue

    except KeyboardInterrupt:
        return(0)

# 创建GUI窗口
root = tk.Tk()

root.title("中控助手")

root.attributes('-topmost', 1)

root.minsize(400, 125)

frame = tk.Frame(root)
frame.place(relx=0.5, rely=0.5, anchor='center')  

# 创建坐标标签
coord_label1 = tk.Label(root, text="x: 0, y: 0", bg="grey")
coord_label1.place(relx=0.25, rely=0.25, x=20, anchor='center')  
coord_label2 = tk.Label(root, text="x: 0, y: 0", bg="grey")
coord_label2.place(relx=0.25, rely=0.5, x=20, anchor='center')  
coord_label3 = tk.Label(root, text="x: 0, y: 0", bg="grey")
coord_label3.place(relx=0.25, rely=0.75, x=20, anchor='center')  

frame = tk.Frame(root)
frame.place(relx=0.75, rely=0.5, anchor='center') 

# 创建按钮
copy_button = tk.Button(frame, text="选择坐标", command=copy_coord)
copy_button.pack(side=tk.TOP, pady=(50, 10))  

start_button = tk.Button(frame, text="开始", command=start_program)
start_button.pack(side=tk.TOP, pady=(10, 10))  
stop_button = tk.Button(frame, text="停止", command=stop_program)
stop_button.pack(side=tk.TOP, pady=(10, 50))  

# 启动GUI主循环
root.mainloop()