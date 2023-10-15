import threading
import time
import tkinter as tk
from tkinter import ttk
import pyautogui
from pynput.mouse import Listener as MouseListener


class AutoClicker:
    def __init__(self, root):
        self.root = root
        self.root.title("AutomaticClick-12H")
        self.root.geometry("350x150")
        self.root.resizable(False, False)
        self.root.attributes('-topmost', 1)

        self.coord_x1, self.coord_y1, self.coord_x2, self.coord_y2, self.coord_x3, self.coord_y3 = 0, 0, 0, 0, 0, 0
        self.keyboard_active = False

        self.style = ttk.Style()
        self.style.configure("TLabel", background="#ffffff")

        self.create_ui()

    def create_ui(self):
        frame = tk.Frame(self.root)
        frame.place(relx=0.5, rely=0.5, anchor='center')

        self.coord_label1 = ttk.Label(self.root, text="[2链坐标] x: 0, y: 0", style='TLabel')
        self.coord_label1.place(relx=0.25, rely=0.3, anchor='center')
        self.coord_label2 = ttk.Label(self.root, text="[1链坐标] x: 0, y: 0", style='TLabel')
        self.coord_label2.place(relx=0.25, rely=0.5, anchor='center')
        self.coord_label3 = ttk.Label(self.root, text="[订单查询] x: 0, y: 0", style='TLabel')
        self.coord_label3.place(relx=0.25, rely=0.7, anchor='center')

        frame = tk.Frame(self.root)
        frame.place(relx=0.75, rely=0.5, anchor='center')

        copy_button = ttk.Button(frame, text="选择坐标", command=self.copy_coord)
        copy_button.pack(side=tk.TOP, pady=(20, 5))
        start_button = ttk.Button(frame, text="开始", command=self.start_program)
        start_button.pack(side=tk.TOP, pady=(5, 5))
        stop_button = ttk.Button(frame, text="停止", command=self.stop_program)
        stop_button.pack(side=tk.TOP, pady=(5, 20))

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
            else:
                self.coord_x3, self.coord_y3 = x, y
                self.coord_label3.config(text="x: {}, y: {}".format(self.coord_x3, self.coord_y3))
                return False

    def copy_coord(self):
        listener = MouseListener(on_click=self.on_click)
        listener.start()

    def start_program(self):
        threading.Thread(target=self.your_program).start()

    def stop_program(self):
        self.end_time = time.time()

    def your_program(self):
        pyautogui.FAILSAFE = False
        time.sleep(5)
        try:
            end_time = time.time() + 720 * 60
            while time.time() < end_time:
                try:
                    pyautogui.moveTo(self.coord_x1, self.coord_y1)
                    pyautogui.click()

                    pyautogui.moveTo(self.coord_x2, self.coord_y2)
                    pyautogui.click()
                    time.sleep(5)

                    pyautogui.moveTo(self.coord_x3, self.coord_y3)
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
