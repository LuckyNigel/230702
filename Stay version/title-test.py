import tkinter as tk
from tkinter import ttk

class CustomWindow:
    def __init__(self, root):
        self.root = root
        self.root.title("自定义窗口")
        self.root.geometry("465x245")

        # 获取屏幕的宽度和高度
        screen_width = root.winfo_screenwidth()
        screen_height = root.winfo_screenheight()

        # 计算窗体的左上角位置，使其居中
        window_width = 300
        window_height = 200
        x = (screen_width - window_width) // 2
        y = (screen_height - window_height) // 2

        # 设置窗体的位置
        self.root.geometry(f"{window_width}x{window_height}+{x}+{y}")

        # 隐藏默认窗口标题栏
        self.root.overrideredirect(True)

        # 创建ttk样式
        style = ttk.Style()
        style.configure("TitleLabel.TLabel", font=("Segoe UI", 12), background="#a2aab3", foreground="#000000")
        style.configure("CloseButton.TButton", font=("Segoe UI", 12), foreground="#000000")
        style.configure("Left.TFrame", background="#a2aab3")  # 配置左侧区域的样式

        # 创建标题栏
        self.create_title_bar()

        # 绑定鼠标事件来实现拖动窗口
        self.offset_x = 0
        self.offset_y = 0
        self.title_frame.bind("<ButtonPress-1>", self.on_press)
        self.title_frame.bind("<B1-Motion>", self.on_drag)
        self.title_frame.bind("<ButtonRelease-1>", self.on_release)

    def create_title_bar(self):
        # 创建一个标题栏的Frame
        self.title_frame = ttk.Frame(self.root, height=20)
        self.title_frame.pack(fill=tk.X)

        # 创建一个右侧区域，包含关闭按钮，大小为正方形1：1，显示"X"
        right_frame = ttk.Frame(self.title_frame, width=20, height=20)
        right_frame.pack(side=tk.RIGHT)

        close_button = ttk.Button(right_frame, text="X", command=self.close_window, style="CloseButton.TButton")
        close_button.pack(fill=tk.BOTH)

        # 创建一个左侧区域，底色为a2aab3，内容显示为"标题测试-2"
        left_frame = ttk.Frame(self.title_frame, style="Left.TFrame")
        left_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        title_label = ttk.Label(left_frame, text="标题测试-2", style="TitleLabel.TLabel")
        title_label.pack(padx=5, pady=5)

        # 绑定鼠标事件到left_frame和title_label
        left_frame.bind("<ButtonPress-1>", self.on_press)
        left_frame.bind("<B1-Motion>", self.on_drag)
        left_frame.bind("<ButtonRelease-1>", self.on_release)

        title_label.bind("<ButtonPress-1>", self.on_press)
        title_label.bind("<B1-Motion>", self.on_drag)
        title_label.bind("<ButtonRelease-1>", self.on_release)

    def on_drag(self, event):
        x, y = event.x_root, event.y_root
        self.root.geometry(f"+{x - self.offset_x}+{y - self.offset_y}")

    def on_press(self, event):
        self.offset_x = event.x_root - self.root.winfo_x()
        self.offset_y = event.y_root - self.root.winfo_y()

    def on_release(self, event):
        self.offset_x = 0
        self.offset_y = 0

    def close_window(self):
        self.root.destroy()

if __name__ == "__main__":
    root = tk.Tk()
    window = CustomWindow(root)
    root.mainloop()