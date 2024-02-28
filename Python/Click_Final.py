import threading
import time
import tkinter as tk
from tkinter import ttk
import pyautogui
from pynput.mouse import Listener as MouseListener
import tkinter.messagebox as messagebox


class AutoClickerApp:
    def __init__(self, root_windows):
        self.root = root_windows
        self.root.title("讲解点击-终极版")
        self.root.attributes('-topmost', 1)
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)
        self.root.geometry("690x170")
        self.root.resizable(False, False)

        self.coord_x1, self.coord_y1, self.coord_x2, self.coord_y2, self.coord_x3, self.coord_y3 = 0, 0, 0, 0, 0, 0
        self.end_time = None
        self.keyboard_active = False
        self.click_duration = 0

    #     self.create_gui()
    #
    # def create_gui(self):
        frame = tk.Frame(self.root)
        frame.pack(pady=25)

        self.coord_label1 = tk.Label(frame, text="[2链坐标] x: 0, y: 0", bg="#dedede")
        self.coord_label1.pack(side=tk.LEFT, padx=(10, 10))
        self.coord_label2 = tk.Label(frame, text="[1链坐标] x: 0, y: 0", bg="#dedede")
        self.coord_label2.pack(side=tk.LEFT, padx=(10, 10))
        self.coord_label3 = tk.Label(frame, text="[查询坐标] x: 0, y: 0", bg="#dedede")
        self.coord_label3.pack(side=tk.LEFT, padx=(10, 10))

        frame_options = tk.Frame(self.root)
        frame_options.pack(pady=25)

        copy_button = tk.Button(frame_options, text="选择坐标", command=self.copy_coord)
        copy_button.pack(side=tk.LEFT, padx=(10, 10))

        self.click_options_type = tk.StringVar()
        self.click_options_type.set("弹窗")
        popup_radio = ttk.Radiobutton(frame_options, text="弹窗", variable=self.click_options_type, value="弹窗")
        stay_radio = ttk.Radiobutton(frame_options, text="常驻", variable=self.click_options_type, value="常驻")
        popup_radio.pack(side=tk.LEFT, padx=(10, 10))
        stay_radio.pack(side=tk.LEFT, padx=(10, 10))

        self.click_options = tk.IntVar()
        self.click_options.set(14)
        popup_time_label = tk.Label(frame_options, text="循环时长(小时) =")
        popup_time_label.pack(side=tk.LEFT, padx=(10, 10))
        popup_time_option = ttk.Combobox(frame_options, textvariable=self.click_options, values=(7, 11, 14), width=4)
        popup_time_option.state(["readonly"])
        popup_time_option.pack(side=tk.LEFT, padx=(10, 10))

        start_button = tk.Button(frame_options, text="开始", command=self.start_program)
        start_button.pack(side=tk.LEFT, padx=(10, 10))
        stop_button = tk.Button(frame_options, text="停止", command=self.stop_program)
        stop_button.pack(side=tk.LEFT, padx=(10, 10))

    def copy_coord(self):
        listener = MouseListener(on_click=self.on_click)
        listener.start()

    def on_click(self, x, y, button, pressed):
        if pressed:
            if self.coord_x1 == self.coord_y1 == 0:
                self.coord_x1, self.coord_y1 = x, y
                self.coord_label1.config(text="[2链] x: {}, y: {}".format(self.coord_x1, self.coord_y1))
            elif self.coord_x2 == self.coord_y2 == 0:
                self.coord_x2, self.coord_y2 = x, y
                self.coord_label2.config(text="[1链] x: {}, y: {}".format(self.coord_x2, self.coord_y2))
            else:
                self.coord_x3, self.coord_y3 = x, y
                self.coord_label3.config(text="[查询] x: {}, y: {}".format(self.coord_x3, self.coord_y3))
                return False

    def on_key_press(self, key):
        self.keyboard_active = True

    def on_key_release(self, key):
        self.keyboard_active = False

    def start_program(self):
        self.click_duration = self.click_options.get()
        if self.click_options_type.get() == "弹窗":
            threading.Thread(target=self.click_popup).start()
            threading.Thread(target=self.update_title).start()
        elif self.click_options_type.get() == "常驻":
            threading.Thread(target=self.click_stay).start()
            threading.Thread(target=self.update_title).start()

    def stop_program(self):
        self.end_time = time.time()
        self.root.title("讲解点击-终极版")

    def update_title(self):
        remaining_time = self.click_duration * 3600
        while remaining_time > 0:
            minutes = remaining_time // 60
            seconds = remaining_time % 60
            self.root.title(
                "讲解点击-->当前模式 : {}--> {:02d}:{:02d} <--".format(self.click_options_type.get(), minutes, seconds))
            remaining_time -= 1
            time.sleep(1)
            if self.end_time is not None and time.time() >= self.end_time:
                break

    def click_popup(self):
        pyautogui.FAILSAFE = False
        time.sleep(5)
        try:
            self.end_time = time.time() + self.click_duration * 3600
            while time.time() < self.end_time:
                try:
                    pyautogui.moveTo(self.coord_x1, self.coord_y1)
                    pyautogui.click()
                    pyautogui.moveTo(self.coord_x2, self.coord_y2)
                    pyautogui.click()
                    time.sleep(9.7)
                    pyautogui.moveTo(self.coord_x3, self.coord_y3)
                    pyautogui.click()
                    time.sleep(1)
                except pyautogui.FailSafeException:
                    while True:
                        time.sleep(5)
                        if self.mouse.position == (self.coord_x1, self.coord_y1) and not self.keyboard_active:
                            break
                    self.keyboard_active = False
                continue
        except KeyboardInterrupt:
            return 0

    def click_stay(self):
        pyautogui.FAILSAFE = False
        time.sleep(5)
        try:
            self.end_time = time.time() + self.click_duration * 60
            while time.time() < self.end_time:
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
                        if self.mouse.position == (self.coord_x1, self.coord_y1) and not self.keyboard_active:
                            break
                    self.keyboard_active = False
                continue
        except KeyboardInterrupt:
            return 0

    def on_closing(self):
        if messagebox.askokcancel("**  二次确认  **",
                                  "------------------------\n软件开源免费\n请您遵循MIT开源协议\n------------------------\n你确定要终止进程吗？"):
            self.stop_program()
            self.root.destroy()


if __name__ == "__main__":
    root = tk.Tk()
    app = AutoClickerApp(root)
    root.mainloop()
