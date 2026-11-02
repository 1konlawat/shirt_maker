import os
import shutil
from moviepy import VideoFileClip

# 1. กำหนด Path ของโฟลเดอร์ทั้ง 3 (ใช้ r"" ด้านหน้าเพื่อจัดการเรื่อง Backslash ใน Windows)
source_dir = r"C:\Users\KK_KK\OneDrive - Rajamangala University of Technology Phranakhon\เดสก์ท็อป\shirt_maker\shirts\แยกไฟล์\ไฟล์รวม"
under_1s_dir = r"C:\Users\KK_KK\OneDrive - Rajamangala University of Technology Phranakhon\เดสก์ท็อป\shirt_maker\shirts\แยกไฟล์\ต่ำกว่า1วิ"
over_1s_dir = r"C:\Users\KK_KK\OneDrive - Rajamangala University of Technology Phranakhon\เดสก์ท็อป\shirt_maker\shirts\แยกไฟล์\สูงกว่า1วิ"

# สร้างโฟลเดอร์ปลายทางเตรียมไว้ในกรณีที่ยังไม่มี
os.makedirs(under_1s_dir, exist_ok=True)
os.makedirs(over_1s_dir, exist_ok=True)

# นามสกุลไฟล์ที่ต้องการให้สคริปต์อ่าน (เพิ่มลดได้ตามต้องการ)
video_exts = ('.mp4', '.avi', '.mov', '.mkv', '.webm')

# ลูปอ่านไฟล์ทั้งหมดในโฟลเดอร์รวม
for filename in os.listdir(source_dir):
    if filename.lower().endswith(video_exts):
        file_path = os.path.join(source_dir, filename)
        
        try:
            # ใช้ moviepy อ่านไฟล์เพื่อดึงความยาว (duration)
            clip = VideoFileClip(file_path)
            duration = clip.duration
            clip.close() # ปิดคืนหน่วยความจำทันทีที่ได้ค่า
            
            # 2. เงื่อนไขการคัดแยกไฟล์
            if duration < 1.0:
                dest_path = os.path.join(under_1s_dir, filename)
                shutil.move(file_path, dest_path)
                print(f"[< 1 วิ] ย้ายไฟล์สำเร็จ: {filename} (ความยาว {duration:.2f} วินาที)")
            else:
                dest_path = os.path.join(over_1s_dir, filename)
                shutil.move(file_path, dest_path)
                print(f"[>= 1 วิ] ย้ายไฟล์สำเร็จ: {filename} (ความยาว {duration:.2f} วินาที)")
                
        except Exception as e:
            print(f"เกิดข้อผิดพลาดกับไฟล์ {filename}: {e}")

print("\n--- คัดแยกไฟล์เสร็จสมบูรณ์ ---")