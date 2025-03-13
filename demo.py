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
root.geometry("200x200")  # Thiết lập kích thước cửa sổ 200px x 200px
root.configure(bg='red')

# Biến toàn cục để lưu tên người dùng
user_name = ""
name_image = "screenshot.png"
# Hàm tải lên ảnh tới Cloudinary
def upload_to_cloudinary(file_path, public_id):
    url = "https://api.cloudinary.com/v1_1/dudtrotnp/image/upload"
    
    with open(file_path, 'rb') as file:
        files = {'file': file}
        data = {
            'upload_preset': "md05_project",
            'public_id': public_id  # Đặt tên tệp ở đây
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

# Hàm chụp màn hình
def capture_screen():
    global name_image  # Thêm dòng này
    screenshot = pyautogui.screenshot()
    if screenshot is not None:
        name_image = user_name + ".png"
        screenshot.save(name_image)
# Hàm kiểm tra có mẫu trong ảnh chụp hay không
def check_image_presence(template_path, screenshot_path):
    template = cv2.imread(template_path)
    screenshot = cv2.imread(screenshot_path)

    if template is None or screenshot is None:
        print("Không thể đọc ảnh mẫu hoặc ảnh chụp.")
        return False

    template_gray = cv2.cvtColor(template, cv2.COLOR_BGR2GRAY)
    screenshot_gray = cv2.cvtColor(screenshot, cv2.COLOR_BGR2GRAY)

    result = cv2.matchTemplate(screenshot_gray, template_gray, cv2.TM_CCOEFF_NORMED)
    threshold = 0.8  # Ngưỡng xác định sự khớp
    locations = np.where(result >= threshold)

    return len(locations[0]) > 0

# Khai báo biến toàn cục
exitProgram = False 

# Hàm thực hiện công việc
def task():
    global exitProgram
    capture_screen()
    if check_image_presence(template_path1, name_image):
        winsound.Beep(frequency, duration)
        print("Đã phát hiện mẫu 1.")
        upload_to_cloudinary(name_image, f"{user_name}_sample1")  
        exitProgram = True
    elif check_image_presence(template_path2, name_image):
        winsound.Beep(frequency, duration)
        print("Đã phát hiện mẫu 2.")
        upload_to_cloudinary(name_image, f"{user_name}_sample2")  
        exitProgram = True

# Đường dẫn tới ảnh mẫu
template_path1 = "./image/poe.png"
template_path2 = "./image/chatgpt.png"

# Hàm khởi động chương trình
def start_program():
    global user_name
    user_name = entry.get()  # Lấy tên người dùng từ ô input
    btn_start.pack_forget()  # Ẩn nút Start
    entry.pack_forget()      # Ẩn ô input
    schedule.every(2).seconds.do(task)  # Lập lịch công việc

    # Vòng lặp chính
    while not exitProgram:
        schedule.run_pending()  
        time.sleep(1)

# Tạo ô input
entry = tk.Entry(root, font=('Helvetica', 16))
entry.pack(pady=20)  # Thêm khoảng cách

# Tạo nút Start
btn_start = tk.Button(root, text="Start", command=start_program, bg='green', font=('Helvetica', 16))
btn_start.pack(expand=True)

# Chạy cửa sổ Tkinter
root.mainloop()