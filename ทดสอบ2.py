import cv2
import numpy as np
import os

# กำหนดโฟลเดอร์ต้นทาง
folder_path = r"C:\Users\KK_KK\OneDrive - Rajamangala University of Technology Phranakhon\เดสก์ท็อป\ทดสอบ"

# สร้างโฟลเดอร์ใหม่สำหรับเก็บไฟล์ผลลัพธ์
output_folder = os.path.join(folder_path, "transparent_stickers")
os.makedirs(output_folder, exist_ok=True) # สร้างโฟลเดอร์ถ้ายังไม่มี

print(f"กำลังเริ่มค้นหาและแปลงไฟล์ในโฟลเดอร์:\n{folder_path}\n" + "-"*40)

success_count = 0

# วนลูปอ่านทุกไฟล์ที่อยู่ในโฟลเดอร์
for filename in os.listdir(folder_path):
    
    # กรองทำเฉพาะไฟล์ภาพ (ไม่ต้องเช็ค _transparent แล้ว เพราะเราแยกโฟลเดอร์เก็บ)
    if filename.lower().endswith(('.jpg', '.jpeg', '.png')):
        
        input_path = os.path.join(folder_path, filename)
        
        # ดึงแค่ชื่อไฟล์ไม่เอานามสกุล เพื่อเอามาสร้างชื่อไฟล์ใหม่
        name_without_ext = os.path.splitext(filename)[0]
        output_filename = f"{name_without_ext}_transparent.png"
        
        # เซ็ตให้บันทึกไฟล์ลงในโฟลเดอร์ใหม่ที่สร้างขึ้น
        output_path = os.path.join(output_folder, output_filename)
        
        try:
            # โหลดภาพด้วย numpy
            img_array = np.fromfile(input_path, np.uint8)
            img = cv2.imdecode(img_array, cv2.IMREAD_COLOR)
            
            if img is None:
                # ถ้าโฟลเดอร์ transparent_stickers โผล่มาในการวนลูป img จะเป็น None ให้ข้ามไป
                continue 
            
            # 1. แปลงเป็นขาวดำเพื่อดึงค่าความสว่าง
            gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
            
            # 2. ใช้ความสว่างเป็นความโปร่งใส (Alpha)
            alpha = gray
            
            # 3. กำหนดตัวสติกเกอร์ให้เป็นสีขาวล้วน
            b = np.full_like(gray, 255)
            g = np.full_like(gray, 255)
            r = np.full_like(gray, 255)
            
            # 4. รวมช่องสี RGB + Alpha
            rgba = cv2.merge([b, g, r, alpha])
            
            # บันทึกภาพด้วย numpy
            is_success, buffer = cv2.imencode(".png", rgba)
            if is_success:
                buffer.tofile(output_path)
                print(f"[สำเร็จ] {filename}  =>  เก็บไว้ที่ transparent_stickers/{output_filename}")
                success_count += 1
            else:
                print(f"[ล้มเหลว] เกิดข้อผิดพลาดตอนบันทึก: {filename}")
                
        except Exception as e:
            print(f"[Error] ไฟล์ {filename}: {e}")

print("-" * 40)
print(f"เสร็จสิ้นการทำงาน! แปลงไฟล์สำเร็จทั้งหมด {success_count} ไฟล์")
print(f"เข้าไปดูไฟล์สติกเกอร์ทั้งหมดได้ที่โฟลเดอร์:\n{output_folder}")