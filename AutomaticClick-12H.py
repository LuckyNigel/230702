import tkinter as tk
from tkinter import ttk
import threading
import time
import pyautogui
from pynput.keyboard import Listener as KeyboardListener
from pynput.mouse import Listener as MouseListener, Controller as MouseController

global coord_x1, coord_y1, coord_x2, coord_y2, coord_x3, coord_y3
coord_x1, coord_y1, coord_x2, coord_y2, coord_x3, coord_y3 = 0, 0, 0, 0, 0, 0

keyboard_active = False


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
            coord_label1.config(text="x: {}, y: {}".format(coord_x1, coord_y1))
        elif coord_x2 == coord_y2 == 0:
            coord_x2, coord_y2 = x, y
            coord_label2.config(text="x: {}, y: {}".format(coord_x2, coord_y2))
        else:
            coord_x3, coord_y3 = x, y
            coord_label3.config(text="x: {}, y: {}".format(coord_x3, coord_y3))
            return False


def copy_coord():
    listener = MouseListener(on_click=on_click)
    listener.start()


def start_program():
    threading.Thread(target=your_program).start()


def stop_program():
    global end_time
    end_time = time.time()


keyboard = MouseController()
mouse = MouseController()


def your_program():
    pyautogui.FAILSAFE = False
    time.sleep(5)
    try:
        global end_time
        end_time = time.time() + 660 * 60
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
        return


root = tk.Tk()
root.title("讲解AutoClink-12H")
root.geometry("350x150")
root.resizable(False, False)
root.attributes('-topmost', 1)

frame = tk.Frame(root)
frame.place(relx=0.5, rely=0.5, anchor='center')

style = ttk.Style()
style.configure("TLabel", background="#ffffff")

coord_label1 = ttk.Label(root, text="[2链坐标] x: 0, y: 0", style='TLabel')
coord_label1.place(relx=0.25, rely=0.25, anchor='center')
coord_label2 = ttk.Label(root, text="[1链坐标] x: 0, y: 0", style='TLabel')
coord_label2.place(relx=0.25, rely=0.5, anchor='center')
coord_label3 = ttk.Label(root, text="订单查询 x: 0, y: 0", style='TLabel')
coord_label3.place(relx=0.25, rely=0.75, anchor='center')

frame = tk.Frame(root)
frame.place(relx=0.75, rely=0.5, anchor='center')

copy_button = ttk.Button(frame, text="选择坐标", command=copy_coord)
copy_button.pack(side=tk.TOP, pady=(20, 5))
start_button = ttk.Button(frame, text="开始", command=start_program)
start_button.pack(side=tk.TOP, pady=(5, 5))
stop_button = ttk.Button(frame, text="停止", command=stop_program)
stop_button.pack(side=tk.TOP, pady=(5, 20))


root.mainloop()
