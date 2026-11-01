import subprocess
import os
import random

# 1. กำหนด Path วิดีโอหลักและไฟล์ผลลัพธ์
main_video = r"C:\Users\KK_KK\OneDrive - Rajamangala University of Technology Phranakhon\เดสก์ท็อป\shirt_maker\outputs\เสื้อขาว_26_26.mp4"
output_video = r"C:\Users\KK_KK\OneDrive - Rajamangala University of Technology Phranakhon\เดสก์ท็อป\shirt_maker\outputs\test_3_stickers_combined.mp4"

# 2. กำหนดค่าเริ่มต้นของแต่ละตำแหน่ง
sticker_configs = [
    {
        "name": "บนขวา",
        "path": r"C:\Users\KK_KK\OneDrive - Rajamangala University of Technology Phranakhon\เดสก์ท็อป\shirt_maker\sticker\ประกอบ\ขวา",
        "scale": 450,
        "overlay": "W-w+150:-100"
    },
    {
        "name": "ตรงกลาง",
        "path": r"C:\Users\KK_KK\OneDrive - Rajamangala University of Technology Phranakhon\เดสก์ท็อป\shirt_maker\sticker\กลาง",
        "scale": 350,
        "overlay": "(W-w)/2:(H-h)/2"
    },
    {
        "name": "ล่างซ้าย",
        "path": r"C:\Users\KK_KK\OneDrive - Rajamangala University of Technology Phranakhon\เดสก์ท็อป\shirt_maker\sticker\ประกอบ\ซ้าย",
        "scale": 500,
        "overlay": "-200:H-h+100"
    }
]

# ฟังก์ชันสุ่มหยิบไฟล์ PNG
def get_random_png(folder_path):
    if not os.path.exists(folder_path):
        return None
    png_files = [file for file in os.listdir(folder_path) if file.lower().endswith('.png')]
    if not png_files:
        return None
    return os.path.join(folder_path, random.choice(png_files))

# 3. ค้นหาสติกเกอร์ที่ใช้งานได้จริง
valid_stickers = []
for config in sticker_configs:
    file_path = get_random_png(config["path"])
    if file_path:
        # ถ้าหาเจอ ให้เก็บข้อมูลไว้เตรียมแปะ
        valid_stickers.append({
            "name": config["name"],
            "file": file_path,
            "scale": config["scale"],
            "overlay": config["overlay"]
        })

# 4. ตรวจสอบและสร้างคำสั่งประกอบวิดีโอ
if not valid_stickers:
    print("ไม่มีสติกเกอร์ในโฟลเดอร์ใดเลย (ข้ามการแปะสติกเกอร์)")
else:
    print("สติกเกอร์ที่สุ่มได้รอบนี้ (อันที่ไม่มีจะถูกข้าม):")
    for st in valid_stickers:
        print(f"- {st['name']}: {os.path.basename(st['file'])}")

    # เริ่มสร้างคำสั่ง FFmpeg
    command = ["ffmpeg", "-y", "-i", main_video]
    
    # ใส่ input (-i) ให้ครบตามจำนวนสติกเกอร์ที่หาเจอ
    for st in valid_stickers:
        command.extend(["-i", st["file"]])
        
    filter_complex = ""
    current_stream = "0:v" # เริ่มต้นจากวิดีโอหลัก
    
    # สร้างเส้นทางฟิลเตอร์ร้อยเรียงกันตามจำนวนที่มี
    for i, st in enumerate(valid_stickers):
        input_idx = i + 1  # 1, 2, 3...
        scale_lbl = f"st{input_idx}"
        out_stream = f"v{input_idx}"
        
        # ปรับขนาด
        filter_complex += f"[{input_idx}:v]scale={st['scale']}:-1[{scale_lbl}];"
        
        # ถ้านี่คือสติกเกอร์อันสุดท้าย ไม่ต้องตั้งชื่อตัวแปรผลลัพธ์ (ปล่อยให้เป็น output คลิปเลย)
        if i == len(valid_stickers) - 1:
            filter_complex += f"[{current_stream}][{scale_lbl}]overlay={st['overlay']}"
        else:
            # ถ้ายังมีสติกเกอร์อันอื่นต่อ ให้ส่งผลลัพธ์ไปที่ [v1], [v2] ...
            filter_complex += f"[{current_stream}][{scale_lbl}]overlay={st['overlay']}[{out_stream}];"
            current_stream = out_stream

    command.extend(["-filter_complex", filter_complex, "-c:a", "copy", output_video])

    print("\nกำลังเรนเดอร์วิดีโอ...")
    subprocess.run(command)
    print(f"เสร็จสิ้น! ดูผลลัพธ์ได้ที่: {output_video}")