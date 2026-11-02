import os
import shutil
from moviepy import VideoFileClip

# 1. กำหนดโฟลเดอร์ต้นทาง
source_dir = r"C:\Users\KK_KK\OneDrive - Rajamangala University of Technology Phranakhon\เดสก์ท็อป\shirt_maker\shirts\เสื้อรวมๅ\mp4_output"

# 2. กำหนดโฟลเดอร์ปลายทาง
dest_hook = r"C:\Users\KK_KK\OneDrive - Rajamangala University of Technology Phranakhon\เดสก์ท็อป\shirt_maker\shirts\เสื้อขาว\ฮุก"
dest_normal = r"C:\Users\KK_KK\OneDrive - Rajamangala University of Technology Phranakhon\เดสก์ท็อป\shirt_maker\shirts\เสื้อขาว\โชว์แบบธรรมดา"
dest_fast = r"C:\Users\KK_KK\OneDrive - Rajamangala University of Technology Phranakhon\เดสก์ท็อป\shirt_maker\shirts\เสื้อขาว\โชว์แบบเร็ว"

# สร้างโฟลเดอร์ปลายทางเตรียมไว้ (หากยังไม่มี)
for folder in [dest_hook, dest_normal, dest_fast]:
    os.makedirs(folder, exist_ok=True)

# 3. วนลูปอ่านไฟล์ .mp4 ในโฟลเดอร์ต้นทาง
for filename in os.listdir(source_dir):
    if filename.lower().endswith(".mp4"):
        file_path = os.path.join(source_dir, filename)
        
        try:
            # ดึงข้อมูลความยาววิดีโอ (วินาที)
            clip = VideoFileClip(file_path)
            duration = clip.duration
            clip.close() # ปิดไฟล์คืนหน่วยความจำ
            
            # 4. คัดกรองและย้ายไฟล์ตามเงื่อนไข (เปลี่ยน shutil.move เป็น shutil.copy ได้ถ้าไม่อยากให้ไฟล์ต้นฉบับหาย)
            if duration >= 3:
                shutil.move(file_path, os.path.join(dest_hook, filename))
                print(f"ย้าย {filename} ({duration:.2f} วิ) -> ฮุก")
            elif duration >= 2:
                shutil.move(file_path, os.path.join(dest_normal, filename))
                print(f"ย้าย {filename} ({duration:.2f} วิ) -> โชว์แบบธรรมดา")
            elif duration >= 1:
                shutil.move(file_path, os.path.join(dest_fast, filename))
                print(f"ย้าย {filename} ({duration:.2f} วิ) -> โชว์แบบเร็ว")
            else:
                print(f"ข้าม {filename} ({duration:.2f} วิ) เพราะสั้นกว่า 1 วินาที")
                
        except Exception as e:
            print(f"เกิดข้อผิดพลาดกับไฟล์ {filename}: {e}")

print("แยกไฟล์เสร็จเรียบร้อยครับ!")