import threading
import time
import tkinter as tk
from tkinter import ttk
import pyautogui
from pynput.keyboard import Controller as KeyboardController
from pynput.keyboard import Listener as KeyboardListener
from pynput.mouse import Controller as MouseController
from pynput.mouse import Listener as MouseListener
import tkinter.messagebox as messagebox

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
            coord_label1.config(text="[2链] x: {}, y: {}".format(coord_x1, coord_y1))
        elif coord_x2 == coord_y2 == 0:
            coord_x2, coord_y2 = x, y
            coord_label2.config(text="[1链] x: {}, y: {}".format(coord_x2, coord_y2))
        else:
            coord_x3, coord_y3 = x, y
            coord_label3.config(text="[查询] x: {}, y: {}".format(coord_x3, coord_y3))
            return False


def copy_coord():
    listener = MouseListener(on_click=on_click)
    listener.start()


def update_title():
    remaining_time = click_duration * 3600
    while remaining_time > 0:
        minutes = remaining_time // 60
        seconds = remaining_time % 60
        root.title("讲解点击-{}版 - {:02d}:{:02d}".format(click_options_type.get(), minutes, seconds))
        remaining_time -= 1
        time.sleep(1)


def start_program():
    global click_duration
    if click_duration == 0:
        click_duration = click_options.get()

    if click_options_type.get() == "弹窗":
        threading.Thread(target=click_popup).start()
        threading.Thread(target=update_title).start()
    elif click_options_type.get() == "常驻":
        threading.Thread(target=click_stay).start()
        threading.Thread(target=update_title).start()


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
        end_time = time.time() + click_duration * 3600
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
        return 0


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


def on_closing():
    if messagebox.askokcancel("二次确认", "你确定要终止进程吗？"):
        # 用户点击确认关闭
        stop_program()  # 停止点击操作
        root.destroy()


root = tk.Tk()
root.title("讲解点击-终极版")
root.attributes('-topmost', 1)
root.protocol("WM_DELETE_WINDOW", on_closing)  # 关联关闭窗口操作
# 设置窗口大小
root.geometry("690x170")  # 增加高度以容纳间隔
# 禁止窗口缩放
root.resizable(False, False)
# 创建一个Frame用于放置所有组件
frame = tk.Frame(root)
frame.pack(pady=25)  # 设置上下间隔为25像素

coord_label1 = tk.Label(frame, text="[2链坐标] x: 0, y: 0", bg="#dedede")
coord_label1.pack(side=tk.LEFT, padx=(10, 10))
coord_label2 = tk.Label(frame, text="[1链坐标] x: 0, y: 0", bg="#dedede")
coord_label2.pack(side=tk.LEFT, padx=(10, 10))
coord_label3 = tk.Label(frame, text="[查询坐标] x: 0, y: 0", bg="#dedede")
coord_label3.pack(side=tk.LEFT, padx=(10, 10))

# 创建一个Frame用于放置选择坐标和其他操作
frame_options = tk.Frame(root)
frame_options.pack(pady=25)  # 设置上下间隔为25像素

copy_button = tk.Button(frame_options, text="选择坐标", command=copy_coord)
copy_button.pack(side=tk.LEFT, padx=(10, 10))

click_options_type = tk.StringVar()
click_options_type.set("弹窗")
popup_radio = ttk.Radiobutton(frame_options, text="弹窗", variable=click_options_type, value="弹窗")
stay_radio = ttk.Radiobutton(frame_options, text="常驻", variable=click_options_type, value="常驻")
popup_radio.pack(side=tk.LEFT, padx=(10, 10))
stay_radio.pack(side=tk.LEFT, padx=(10, 10))

click_options = tk.IntVar()
click_options.set(14)  # 默认为14小时
popup_time_label = tk.Label(frame_options, text="循环时长(小时) =")
popup_time_label.pack(side=tk.LEFT, padx=(10, 10))
popup_time_option = ttk.Combobox(frame_options, textvariable=click_options, values=(7, 11, 14), width=4)  # 设置宽度
# 禁止选择框输入文本
popup_time_option.state(["readonly"])
popup_time_option.pack(side=tk.LEFT, padx=(10, 10))

start_button = tk.Button(frame_options, text="开始", command=start_program)
start_button.pack(side=tk.LEFT, padx=(10, 10))
stop_button = tk.Button(frame_options, text="停止", command=stop_program)
stop_button.pack(side=tk.LEFT, padx=(10, 10))

root.mainloop()
