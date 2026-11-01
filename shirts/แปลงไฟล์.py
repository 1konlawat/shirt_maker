import os
import subprocess
from pathlib import Path

# Path โฟลเดอร์ของคุณ (ใส่ r ไว้ข้างหน้าเพื่อให้อ่าน Backslash ได้ถูกต้อง)
input_folder = r"C:\Users\KK_KK\OneDrive - Rajamangala University of Technology Phranakhon\เดสก์ท็อป\shirt_maker\shirts\เสื้อรวมๅ"

# สร้างโฟลเดอร์ mp4_output ไว้ข้างในโฟลเดอร์เดิม
output_folder = os.path.join(input_folder, "mp4_output")
os.makedirs(output_folder, exist_ok=True)

# เริ่มแปลงไฟล์ .mov เป็น .mp4
for file_path in Path(input_folder).glob("*.mov"):
    output_path = os.path.join(output_folder, f"{file_path.stem}.mp4")
    
    command = [
        "ffmpeg", "-i", str(file_path),
        "-c", "copy",
        str(output_path)
    ]
    
    subprocess.run(command)
    print(f"แปลง {file_path.name} เสร็จแล้ว")

print("แปลงไฟล์ทั้งโฟลเดอร์เสร็จสมบูรณ์!")