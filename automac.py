import tkinter as tk
import pyautogui
import time
import threading

# 设置点击的坐标
x = 100
y = 200

# Create a function to start the program
def start_program():
    global running
    running = True
    # Create a new thread to run the program
    thread = threading.Thread(target=run_program)
    thread.start()

# Create a function to stop the program
def stop_program():
    global running
    running = False

# Create a function to run the program
def run_program():
    while running:
        # 获取当前鼠标位置
        current_x, current_y = pyautogui.position()

        # 如果鼠标位置与目标位置不一致，则移动鼠标到目标位置
        if current_x != x or current_y != y:
            pyautogui.moveTo(x, y)
            # Add your indented block of code here

        # 点击鼠标
        pyautogui.click()

        # 等待一段时间
        time.sleep(5)

# Create the main window
window = tk.Tk()
window.title("Mouse Click Program")
window.geometry("300x200")

# Create a frame for the buttons
button_frame = tk.Frame(window)
button_frame.pack(pady=20)

# Create the start button
start_button = tk.Button(button_frame, text="Start", command=start_program)
start_button.pack(side=tk.LEFT, padx=10)

# Create the stop button
stop_button = tk.Button(button_frame, text="Stop", command=stop_program)
stop_button.pack(side=tk.LEFT, padx=10)

# Set the initial running state
running = False

# Start the main event loop
window.mainloop()