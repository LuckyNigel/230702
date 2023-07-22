import ctypes
import pyautogui
import time

# 隐藏命令行窗口
ctypes.windll.user32.ShowWindow(ctypes.windll.kernel32.GetConsoleWindow(), 0)

# 关闭安全特性
pyautogui.FAILSAFE = False

# 延迟5秒启动
time.sleep(5)

try:
    # 循环持续10分钟
    end_time = time.time() + 10*60  # 10分钟后的时间
    while time.time() < end_time:
        try:
            # 移动鼠标到指定位置
            pyautogui.moveTo(2471, 650)

            # 在当前位置点击鼠标
            pyautogui.click()

            # 等待6秒
            time.sleep(6)

            # 再次点击
            pyautogui.click()

            # 等待2秒
            time.sleep(2)

        except pyautogui.FailSafeException:
            print("检测到鼠标异常,程序将在10秒后重新启动")
            time.sleep(20)
            continue

except KeyboardInterrupt:
    print("程序被用户手动停止")