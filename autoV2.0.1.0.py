import tkinter as tk
import time
import threading
import pyautogui
from pynput.mouse import Listener as MouseListener
from pynput.keyboard import Listener as KeyboardListener

class AutoClickerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("中控助手")  # 设置窗体标题为“中控助手”
        self.root.geometry("400x200")
        #self.root.overrideredirect(True)  # 取消窗体上边框

        # 实现窗体拖动
        self.drag_data = {"x": 0, "y": 0}
        self.root.bind("<ButtonPress-1>", self.start_drag)
        self.root.bind("<B1-Motion>", self.drag)

        self.coordinates = []
        self.click_interval = 1
        self.stop_flag = False
        self.last_activity_time = time.time()

        self.left_frame = tk.Frame(root, bg="gray")
        self.left_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        self.coord_label1 = tk.Label(self.left_frame, text="坐标1：", bg="gray")
        self.coord_label1.pack(pady=5)
        self.coord_label2 = tk.Label(self.left_frame, text="坐标2：", bg="gray")
        self.coord_label2.pack(pady=5)
        self.coord_label3 = tk.Label(self.left_frame, text="坐标3：", bg="gray")
        self.coord_label3.pack(pady=5)

        self.right_frame = tk.Frame(root)
        self.right_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)

        self.select_btn = tk.Button(self.right_frame, text="选择坐标", command=self.select_coordinates)
        self.select_btn.pack(pady=10)
        self.start_btn = tk.Button(self.right_frame, text="开始", command=self.start_auto_click)
        self.start_btn.pack(pady=10)
        self.stop_btn = tk.Button(self.right_frame, text="停止", command=self.stop_auto_click)
        self.stop_btn.pack(pady=10)

    def start_drag(self, event):
        # 开始拖动
        self.drag_data["x"] = event.x
        self.drag_data["y"] = event.y

    def drag(self, event):
        # 拖动窗体
        x = event.x - self.drag_data["x"]
        y = event.y - self.drag_data["y"]
        self.root.geometry(f"+{self.root.winfo_x() + x}+{self.root.winfo_y() + y}")

    def close_window(self):
        # 关闭窗口
        self.root.destroy()

    def minimize_window(self):
        # 最小化窗口
        self.root.iconify()

    def select_coordinates(self):
        self.coordinates = []
        self.coord_label1.config(text="坐标1：")
        self.coord_label2.config(text="坐标2：")
        self.coord_label3.config(text="坐标3：")
        self.root.bind("<Button-1>", self.get_mouse_coordinates)

    def get_mouse_coordinates(self, event):
        if len(self.coordinates) < 3:
            self.coordinates.append((event.x, event.y))

            if len(self.coordinates) == 1:
                self.coord_label1.config(text=f"坐标1：{event.x}, {event.y}")
            elif len(self.coordinates) == 2:
                self.coord_label2.config(text=f"坐标2：{event.x}, {event.y}")
            else:
                self.coord_label3.config(text=f"坐标3：{event.x}, {event.y}")

            if len(self.coordinates) == 3:
                self.root.unbind("<Button-1>")


    def start_auto_click(self):
        # 添加监听鼠标和键盘的线程
        self.mouse_listener = MouseListener(on_move=self.on_mouse_move, on_click=self.on_mouse_click)
        self.keyboard_listener = KeyboardListener(on_press=self.on_keyboard_press)

        self.mouse_listener.start()
        self.keyboard_listener.start()

        self.stop_flag = False
        threading.Thread(target=self.auto_click_loop).start()

    def stop_auto_click(self):
        # 停止监听鼠标和键盘的线程
        self.mouse_listener.stop()
        self.keyboard_listener.stop()

        self.stop_flag = True

    def on_mouse_move(self, x, y):
        # 鼠标移动事件
        self.last_activity_time = time.time()

    def on_mouse_click(self, x, y, button, pressed):
        # 鼠标点击事件
        self.last_activity_time = time.time()

    def on_keyboard_press(self, key):
        # 键盘按键事件
        self.last_activity_time = time.time()

    def auto_click_loop(self):
        while not self.stop_flag:
            # 检查上一次活动时间是否超过5秒，如果超过则继续自动点击
            if time.time() - self.last_activity_time > 5:
                for coord in self.coordinates:
                    pyautogui.click(coord[0], coord[1])
                    time.sleep(self.click_interval)

if __name__ == "__main__":
    root = tk.Tk()
    app = AutoClickerApp(root)
    root.mainloop()
