import time
import schedule
import pyautogui
import cv2
import numpy as np
import os
import requests
import tkinter as tk
import winsound

# Tần số và thời gian cho âm thanh
frequency = 1000  # Tần số (Hz)
duration = 1000   # Thời gian (ms)

# Tạo cửa sổ chính
root = tk.Tk()

def upload_to_cloudinary(file_path):
    url = f"https://api.cloudinary.com/v1_1/dudtrotnp/image/upload"

    with open(file_path, 'rb') as file:
        files = {'file': file}
        data = {
            'upload_preset': "md05_project"
        }

        try:
            print("Đang tải lên Cloudinary...")
            response = requests.post(url, files=files, data=data)
            response.raise_for_status()  # Kiểm tra xem có lỗi hay không

            secure_url = response.json().get('secure_url')
            print("Tải lên thành công. URL an toàn:", secure_url)
            return secure_url
        except requests.exceptions.RequestException as error:
            print("Lỗi khi tải lên:", error)

# Thiết lập kích thước cửa sổ toàn màn hình
root.attributes('-fullscreen', True)

# Đặt màu nền là đỏ
root.configure(bg='red')

# Kết thúc chương trình khi nhấn phím Escape
def exit_fullscreen(event):
    root.quit()  # Thoát khỏi vòng lặp Tkinter

root.bind('<Escape>', exit_fullscreen)

# Hàm chụp màn hình
def capture_screen():
    screenshot = pyautogui.screenshot()
    if screenshot is not None:
        screenshot.save("screenshot.png")

# Hàm kiểm tra xem mẫu có xuất hiện trong ảnh chụp
def check_image_presence(template_path, screenshot_path):
    # Đọc ảnh mẫu và ảnh chụp
    template = cv2.imread(template_path)
    screenshot = cv2.imread(screenshot_path)

    # Kiểm tra xem ảnh có được đọc thành công không
    if template is None or screenshot is None:
        print("Không thể đọc ảnh mẫu hoặc ảnh chụp.")
        return False

    # Chuyển đổi ảnh sang màu xám
    template_gray = cv2.cvtColor(template, cv2.COLOR_BGR2GRAY)
    screenshot_gray = cv2.cvtColor(screenshot, cv2.COLOR_BGR2GRAY)

    # Kiểm tra sự xuất hiện của mẫu
    result = cv2.matchTemplate(screenshot_gray, template_gray, cv2.TM_CCOEFF_NORMED)
    threshold = 0.8  # Ngưỡng xác định sự khớp
    locations = np.where(result >= threshold)

    return len(locations[0]) > 0

# Khai báo biến toàn cục
exitProgram = False 

# Hàm thực hiện công việc
def task():
    global exitProgram  # Khai báo biến toàn cục
    capture_screen()  # Chụp màn hình
    if check_image_presence(template_path1, "screenshot.png"):
        winsound.Beep(frequency, duration)
        print("Đã phát hiện mẫu 1.")
        upload_to_cloudinary("screenshot.png")  
        exitProgram = True  # Đặt biến cờ thành True để dừng chương trình
    elif check_image_presence(template_path2, "screenshot.png"):
        winsound.Beep(frequency, duration)
        print("Đã phát hiện mẫu 2.")
        upload_to_cloudinary("screenshot.png")  
        exitProgram = True  # Đặt biến cờ thành True để dừng chương trình

# Đường dẫn tới ảnh mẫu
template_path1 = "./image/poe.png"
template_path2 = "./image/chatgpt.png"  # Thay đổi theo đường dẫn ảnh mẫu của bạn

# Lập lịch công việc chạy mỗi 2 giây
schedule.every(2).seconds.do(task)

# Vòng lặp chính
try:
    while not exitProgram:  # Tiếp tục chạy khi exitProgram là False
        schedule.run_pending()  
        time.sleep(1)  # Chờ 1 giây trước khi kiểm tra lại
except KeyboardInterrupt:
    print("Chương trình đã dừng.")
finally:
    root.quit()  # Đảm bảo rằng cửa sổ Tkinter sẽ được đóng lại khi thoát