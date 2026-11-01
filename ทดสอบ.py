import cv2
import numpy as np
import os

folder_path = r"C:\Users\KK_KK\OneDrive - Rajamangala University of Technology Phranakhon\เดสก์ท็อป\ทดสอบ"
input_filename = "download (5).jpg" 

input_path = os.path.join(folder_path, input_filename)
output_path = os.path.join(folder_path, "sticker_transparent.png")

try:
    # 1. โหลดภาพด้วย numpy เพื่อแก้ปัญหาโฟลเดอร์ภาษาไทย
    img_array = np.fromfile(input_path, np.uint8)
    img = cv2.imdecode(img_array, cv2.IMREAD_COLOR)
    
    if img is None:
        print(f"ไม่สามารถโหลดภาพได้: {input_path}")
    else:
        # 2. กระบวนการเจาะพื้นดำ
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        
        # ปรับเลข 20 ลง (เช่น 10) ถ้าแสงขอบๆ หายไป / ปรับขึ้น (เช่น 30) ถ้ายังมีคราบสีดำติดมา
        _, alpha = cv2.threshold(gray, 20, 255, cv2.THRESH_BINARY)
        
        b, g, r = cv2.split(img)
        rgba = [b, g, r, alpha]
        transparent_img = cv2.merge(rgba, 4)
        
        # 3. บันทึกภาพด้วย numpy เพื่อแก้ปัญหาโฟลเดอร์ภาษาไทย
        is_success, buffer = cv2.imencode(".png", transparent_img)
        if is_success:
            buffer.tofile(output_path)
            print(f"แปลงภาพเสร็จสิ้น!\nไปเช็คไฟล์ผลลัพธ์ได้ที่: {output_path}")
        else:
            print("เกิดข้อผิดพลาดในการแปลงไฟล์เพื่อบันทึก")
            
except FileNotFoundError:
    print(f"หาไฟล์ไม่พบ: {input_path}\n(ตรวจสอบชื่อไฟล์อีกครั้ง)")