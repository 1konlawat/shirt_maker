import os
import random
from PIL import Image, ImageDraw, ImageFont

def create_text_image(text, font_dir, output_path, width=1080, height=1920):
    # สร้างพื้นหลังโปร่งใสขนาดเต็มจอ (เพื่อให้ง่ายต่อการ overlay ทับวิดีโอ)
    img = Image.new('RGBA', (width, height), (255, 255, 255, 0))
    draw = ImageDraw.Draw(img)
    
    # ค้นหาไฟล์ฟอนต์ .ttf ในโฟลเดอร์
    # ค้นหาไฟล์ฟอนต์ .ttf ในโฟลเดอร์
    font_path = None
    if os.path.exists(font_dir):
        fonts = [f for f in os.listdir(font_dir) if f.lower().endswith('.ttf')]
        if fonts:
            font_path = os.path.join(font_dir, random.choice(fonts)) # 🌟 เปลี่ยนมาใช้ random.choice()
            
    if not font_path:
        print("⚠️ ไม่พบไฟล์ฟอนต์ .ttf ในโฟลเดอร์ จะใช้ฟอนต์พื้นฐานแทน")
        font_path = "arial.ttf"

    # ระบบ Auto Scale
    max_width = width - 150 # เว้นระยะขอบซ้ายขวา
    font_size = 600  # เริ่มต้นขนาดฟอนต์ใหญ่ๆ
    
    try:
        font = ImageFont.truetype(font_path, font_size)
    except IOError:
        font = ImageFont.load_default()
        
    while True:
        bbox = draw.textbbox((0, 0), text, font=font)
        text_w = bbox[2] - bbox[0]
        if text_w <= max_width or font_size <= 40:
            break
        font_size -= 5
        font = ImageFont.truetype(font_path, font_size)
        
    # คำนวณให้อยู่กึ่งกลางหน้าจอ
    bbox = draw.textbbox((0, 0), text, font=font)
    text_w = bbox[2] - bbox[0]
    text_h = bbox[3] - bbox[1]
    x = (width - text_w) / 2
    y = ((height - text_h) / 2) - 300 # ปรับ + หรือ - ตรงนี้ได้ถ้าอยากให้ข้อความขยับขึ้นลง
    
    # วาดข้อความสีขาว พร้อมขอบสีดำหนา (Stroke) สไตล์คลีนๆ
    draw.text((x, y), text, font=font, fill="white", stroke_width=0, stroke_fill="black")
    
    img.save(output_path)
    return output_path