import threading
import time
import tkinter as tk
from tkinter import ttk  # 使用ttk替换tk
import pyautogui
from pynput.keyboard import Controller as KeyboardController
from pynput.keyboard import Listener as KeyboardListener
from pynput.mouse import Controller as MouseController
from pynput.mouse import Listener as MouseListener

global coord_x1, coord_y1, coord_x2, coord_y2, coord_x3, coord_y3
coord_x1, coord_y1, coord_x2, coord_y2, coord_x3, coord_y3 = 0, 0, 0, 0, 0, 0

keyboard_active = False
click_duration = 0

def on_key_press(key):
    global keyboard_active
    keyboard_active = True

def on_key_release(key):
    global keyboard_active
    keyboard_active = False

keyboard_listener = KeyboardListener(on_press=on_key_press, on_release=on_key_release)
keyboard_listener.start()

def on_click(x, y, button, pressed):
    if pressed:
        global coord_x1, coord_y1, coord_x2, coord_y2, coord_x3, coord_y3
        if coord_x1 == coord_y1 == 0:
            coord_x1, coord_y1 = x, y
            coord_label1.config(text="[2链] x: {}, y: {}".format(coord_x1, coord_y1), style="TLabel")
        elif coord_x2 == coord_y2 == 0:
            coord_x2, coord_y2 = x, y
            coord_label2.config(text="[1链] x: {}, y: {}".format(coord_x2, coord_y2), style="TLabel")
        else:
            coord_x3, coord_y3 = x, y
            coord_label3.config(text="[查询] x: {}, y: {}".format(coord_x3, coord_y3), style="TLabel")
            return False

def copy_coord():
    listener = MouseListener(on_click=on_click)
    listener.start()

def start_program():
    global click_duration
    if click_duration == 0:
        click_duration = click_options.get()

    if click_options_type.get() == "弹窗":
        threading.Thread(target=click_popup).start()
    elif click_options_type.get() == "常驻":
        threading.Thread(target=click_stay).start()

def stop_program():
    global end_time
    end_time = time.time()

keyboard = KeyboardController()
mouse = MouseController()

def click_popup():
    pyautogui.FAILSAFE = False

    time.sleep(5)

    try:
        global end_time
        end_time = time.time() + click_duration * 60
        while time.time() < end_time:
            try:
                global coord_x1, coord_y1, coord_x2, coord_y2, coord_x3, coord_y3
                pyautogui.moveTo(coord_x1, coord_y1)
                pyautogui.click()

                pyautogui.moveTo(coord_x2, coord_y2)
                pyautogui.click()
                time.sleep(9.7)

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
        return (0)

def click_stay():
    pyautogui.FAILSAFE = False

    time.sleep(5)

    try:
        global end_time
        end_time = time.time() + click_duration * 60
        while time.time() < end_time:
            try:
                global coord_x1, coord_y1, coord_x2, coord_y2, coord_x3, coord_y3
                pyautogui.moveTo(coord_x1, coord_y1)
                pyautogui.click()

                pyautogui.moveTo(coord_x2, coord_y2)
                pyautogui.click()
                time.sleep(5)

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
        return (0)

root = tk.Tk()
root.resizable(False, False)
root.title("讲解点击-弹窗版")

root.attributes('-topmost', 1)

# 计算标签和下方组件的相对位置
label_pady = 20
label_rely = 0.35
options_rely = 0.9

root.geometry("630x135")  # 设置窗口大小

frame = tk.Frame(root)
frame.place(relx=0.5, rely=label_rely, anchor='center')

frame_labels = tk.Frame(root)
frame_labels.place(relx=0.5, rely=label_rely, anchor='center')

coord_label1 = tk.Label(frame_labels, text="[2链] x: 0, y: 0", style="TLabel")
coord_label1.pack(side=tk.LEFT, padx=(10, 10))
coord_label2 = tk.Label(frame_labels, text="[1链] x: 0, y: 0", style="TLabel")
coord_label2.pack(side=tk.LEFT, padx=(10, 10))
coord_label3 = tk.Label(frame_labels, text="[查询] x: 0, y: 0", style="TLabel")
coord_label3.pack(side=tk.LEFT, padx=(10, 10))

frame_options = tk.Frame(root)
frame_options.place(relx=0.5, rely=options_rely, anchor='center')

copy_button = tk.Button(frame_options, text="选择坐标", command=copy_coord)
copy_button.pack(side=tk.LEFT, padx=(10, 10))

click_options_type = tk.StringVar()
click_options_type.set("弹窗")
popup_radio = ttk.Radiobutton(frame_options, text="弹窗", variable=click_options_type, value="弹窗")
stay_radio = ttk.Radiobutton(frame_options, text="常驻", variable=click_options_type, value="常驻")
popup_radio.pack(side=tk.LEFT, padx=(10, 10))
stay_radio.pack(side=tk.LEFT, padx=(10, 10))

click_options = tk.IntVar()
click_options.set(7)  # 默认为7小时
popup_time_label = tk.Label(frame_options, text="循环时长(小时):")
popup_time_label.pack(side=tk.LEFT, padx=(10, 10))
popup_time_option = ttk.Combobox(frame_options, textvariable=click_options, values=(7, 11, 14))
popup_time_option.pack(side=tk.LEFT, padx=(10, 10))

start_button = tk.Button(frame_options, text="开始", command=start_program)
start_button.pack(side=tk.LEFT, padx=(10, 10))
stop_button = tk.Button(frame_options, text="停止", command=stop_program)
stop_button.pack(side=tk.LEFT, padx=(10, 10))

root.mainloop()
