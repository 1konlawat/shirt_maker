from PIL import Image, ImageDraw, ImageFont
import os

def create_dynamic_text(text, font_path, output_path, video_width=1080):
    # 1. กำหนด Safe Zone (ความกว้างข้อความต้องไม่เกิน 85% ของจอ)
    max_text_width = int(video_width * 0.85)
    
    # 2. ตั้งต้นด้วยฟอนต์ไซส์ใหญ่สุด แล้วค่อยๆ หดลง
    font_size = 200 
    font = ImageFont.truetype(font_path, font_size)
    
    # สร้างภาพจำลองเปล่าๆ เพื่อเอาไว้วัดขนาดตัวอักษร
    dummy_img = Image.new("RGBA", (1, 1), (0, 0, 0, 0))
    draw = ImageDraw.Draw(dummy_img)
    
    # 3. ลูป Auto-Scale: ถ้าข้อความกว้างเกินจอ ให้ลดขนาดฟอนต์ลงทีละ 5
    while True:
        bbox = draw.textbbox((0, 0), text, font=font)
        text_w = bbox[2] - bbox[0]
        text_h = bbox[3] - bbox[1]
        
        if text_w <= max_text_width or font_size <= 20:
            break
        font_size -= 5
        font = ImageFont.truetype(font_path, font_size)

    # 4. เผื่อพื้นที่ขอบภาพนิดหน่อย (Padding) ไม่ให้ตัวหนังสือชิดขอบรูปเกินไป
    img_w = int(text_w * 1.2)
    img_h = int(text_h * 1.5)
    
    # 5. สร้างภาพ PNG พื้นหลังโปร่งใสของจริง
    final_img = Image.new("RGBA", (img_w, img_h), (0, 0, 0, 0))
    final_draw = ImageDraw.Draw(final_img)
    
    # คำนวณจุดวาดให้อยู่กึ่งกลางรูป
    x = (img_w - text_w) / 2
    y = (img_h - text_h) / 2
    
    # 6. วาดตัวหนังสือ: สีขาว (fill) และมีขอบสีดำ (stroke_fill) ความหนา 4px
    final_draw.text((x, y), text, font=font, fill="white", stroke_width=4, stroke_fill="black")
    
    # บันทึกไฟล์
    final_img.save(output_path)
    print(f"✅ สร้างรูปข้อความ '{text}' เสร็จแล้ว! (Size: {font_size})")
    return output_path

# ==========================================
# 🧪 โซนทดสอบการทำงาน (ลองรันดูได้เลย)
# ==========================================
if __name__ == "__main__":
    # ใส่ path ฟอนต์ที่คุณโหลดมา (แก้ให้ตรงกับในเครื่อง)
    my_font = "fonts/PlayfulTime-BLBB8.ttf" 
    
    # ลองเทสคำสั้น (มันจะปรับฟอนต์ใหญ่)
    create_dynamic_text("Cool belt", my_font, "test_short.png")
    
    # ลองเทสคำยาว (มันจะหดฟอนต์ให้เล็กลงอัตโนมัติ)
    create_dynamic_text("Baggy jeans กางเกงยีนส์ทรงสวยมาก", my_font, "test_long.png")