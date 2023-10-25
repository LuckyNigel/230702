import tkinter as tk
from tkinter import ttk
from tkinter import messagebox  # 引入messagebox模块
import threading
import time
import pyautogui
from pynput.keyboard import Listener as KeyboardListener
from pynput.mouse import Listener as MouseListener, Controller as MouseController

class AutoClicker:
    def __init__(self, root):
        self.root = root
        self.root.title("讲解Click-12H")
        self.root.geometry("450x225")  # 修改窗体默认大小
        # 锁定窗体禁止缩放
        self.root.resizable(0, 0)
        self.root.protocol("WM_DELETE_WINDOW", self.on_window_close)  # 添加窗体关闭事件处理函数
        self.root.attributes('-topmost', 1)

        self.coord_x1, self.coord_y1, self.coord_x2, self.coord_y2 = 0, 0, 0, 0
        self.keyboard_active = False
        self.running = False  # 添加终止标志

        self.style = ttk.Style()
        self.style.configure("TLabel", background="#ecf5fe")  # 默认标签背景色为浅蓝色

        self.create_ui()

    def create_ui(self):
        # 左侧框架
        left_frame = ttk.Labelframe(self.root, text="坐标标签", width=300, height=250, style="Red.TLabelframe")
        left_frame.place(x=20, y=20)

        self.coord_label1 = ttk.Label(left_frame, text="[1链坐标] x: 0, y: 0", style='TLabel')
        self.coord_label1.grid(row=0, column=0, padx=10, pady=5, sticky='w')
        self.coord_label2 = ttk.Label(left_frame, text="[订单查询] x: 0, y: 0", style='TLabel')
        self.coord_label2.grid(row=1, column=0, padx=10, pady=5, sticky='w')

        # 选择持续时间标签
        duration_label = ttk.Label(left_frame, text="选择持续时间:", style='Red.TLabel')
        duration_label.grid(row=2, column=0, padx=10, pady=5, sticky='w')

        frame = tk.Frame(self.root)
        frame.place(relx=0.75, rely=0.5, anchor='center')

        copy_button = ttk.Button(frame, text="选择坐标", command=self.copy_coord)
        copy_button.pack(side=tk.TOP, pady=(20, 10))
        start_button = ttk.Button(frame, text="开始", command=self.start_program)
        start_button.pack(side=tk.TOP, pady=(10, 10))
        stop_button = ttk.Button(frame, text="停止", command=self.stop_program)
        stop_button.pack(side=tk.TOP, pady=(10, 20))

        # 下拉选择框
        self.duration_var = tk.StringVar()
        duration_combobox = ttk.Combobox(left_frame, textvariable=self.duration_var, values=["4小时", "7小时", "11小时", "13小时"])
        duration_combobox.set("11小时")  # 默认选择11小时
        # 禁止选择框编辑行为
        duration_combobox.configure(state='readonly')
        duration_combobox.grid(row=3, column=0, padx=10, pady=5, sticky='w')

    def on_window_close(self):
        if self.running:
            # 如果程序在运行中，弹出确认对话框
            if messagebox.askokcancel("确认退出", "是否退出程序？"):
                self.stop_program()
                self.root.destroy()
        else:
            self.root.destroy()

    def on_key_press(self, key):
        self.keyboard_active = True

    def on_key_release(self, key):
        self.keyboard_active = False

    def on_click(self, x, y, button, pressed):
        if pressed:
            if self.coord_x1 == self.coord_y1 == 0:
                self.coord_x1, self.coord_y1 = x, y
                self.coord_label1.config(text="x: {}, y: {}".format(self.coord_x1, self.coord_y1))
            elif self.coord_x2 == self.coord_y2 == 0:
                self.coord_x2, self.coord_y2 = x, y
                self.coord_label2.config(text="x: {}, y: {}".format(self.coord_x2, self.coord_y2))
                return False

    def copy_coord(self):
        listener = MouseListener(on_click=self.on_click)
        listener.start()

    def start_program(self):
        if not self.running:
            duration_text = self.duration_var.get()
            duration_hours = 11  # 默认为11小时
            if duration_text == "4小时":
                duration_hours = 4
            elif duration_text == "7小时":
                duration_hours = 7
            elif duration_text == "13小时":
                duration_hours = 13

            self.running = True
            threading.Thread(target=self.your_program, args=(duration_hours,)).start()

    def stop_program(self):
        self.running = False  # 设置终止标志

    def your_program(self, duration_hours):
        pyautogui.FAILSAFE = False
        time.sleep(5)
        try:
            end_time = time.time() + duration_hours * 60 * 60
            while time.time() < end_time and self.running:  # 添加检查终止标志
                try:
                    pyautogui.moveTo(self.coord_x1, self.coord_y1)
                    pyautogui.click()
                    time.sleep(10)

                    pyautogui.moveTo(self.coord_x1, self.coord_y1)
                    pyautogui.click()
                    time.sleep(1)

                    pyautogui.moveTo(self.coord_x1, self.coord_y1)
                    pyautogui.click()
                    time.sleep(1)

                    pyautogui.moveTo(self.coord_x2, self.coord_y2)
                    pyautogui.click()
                    time.sleep(1)

                except pyautogui.FailSafeException:
                    while True:
                        time.sleep(5)
                        if mouse.position == (self.coord_x1, self.coord_y1) and not self.keyboard_active:
                            break
                        self.keyboard_active = False
                    continue

        except KeyboardInterrupt:
            return

if __name__ == "__main__":
    root = tk.Tk()
    app = AutoClicker(root)
    root.mainloop()
