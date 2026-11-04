import os
import json
import random
import scanner
import prompts
import history
import planner
import builder
from text_maker import create_text_image

# 🌟 ระบุเส้นทางไฟล์ JSON และ ฟอนต์
JSON_PATH = r"C:\Users\KK_KK\OneDrive - Rajamangala University of Technology Phranakhon\เดสก์ท็อป\shirt_maker\shirts\text\เสื้อดำ\data.json"
FONT_DIR = r"C:\Users\KK_KK\OneDrive - Rajamangala University of Technology Phranakhon\เดสก์ท็อป\shirt_maker\fonts"

def main():
    print("=== เริ่มโปรแกรม Shirt Maker ===")
    
    # 🌟 โหลดข้อมูลจาก JSON เก็บไว้ในตัวแปร text_data ตั้งแต่เริ่ม
    text_data = {}
    try:
        with open(JSON_PATH, 'r', encoding='utf-8') as f:
            text_data = json.load(f)
    except Exception as e:
        print(f"⚠️ ไม่สามารถโหลดไฟล์ data.json ได้: {e}")

    valid_shirts = scanner.get_valid_shirts()
    result = prompts.get_user_orders(valid_shirts)
    
    if result[0] is None:
        return
        
    orders, use_zoom, use_transition = result
    
    ask_sticker = input("เอาสติกเกอร์ 3 ตำแหน่งด้วยไหม? (y/n): ").strip().lower()
    use_sticker = (ask_sticker == 'y' or ask_sticker == 'yes')
    
    print("\nกรุณาเลือกโหมดการสร้างวิดีโอ:")
    print("1 - โหมดปกติ (เน้นคลิป Normal แช่ภาพนาน)")
    print("2 - โหมดจังหวะเร็ว (เน้นคลิป Fast สับคัท)")
    print("3 - โหมดผสม (ผสม Normal กับ Fast สลับกัน)")
    
    while True:
        try:
            user_choice = int(input("กรอกตัวเลขโหมด (1, 2 หรือ 3): "))
            if user_choice in [1, 2, 3]:
                print(f"✅ เลือกโหมดที่ {user_choice} เรียบร้อยแล้ว\n")
                break 
            else:
                print("❌ กรุณากรอกเฉพาะเลข 1, 2 หรือ 3 เท่านั้น!")
        except ValueError:
            print("❌ กรุณากรอกเป็นตัวเลข!")

    hist_data = history.load_history()
    
    for order in orders:
        shirt_name = order['shirt']
        count = order['count']
        
        # 🌟 เช็คว่าโฟลเดอร์สินค้านี้มีข้อความใน JSON ไหม และถามผู้ใช้ (ถามแค่ครั้งเดียวก่อนลูปทำคลิป)
        use_text = False
        available_messages = []
        if shirt_name in text_data and len(text_data[shirt_name]) > 0:
            available_messages = text_data[shirt_name]
            ask_text = input(f"\n👉 พบข้อความโปรโมท {len(available_messages)} แบบ สำหรับ '{shirt_name}' \nต้องการเปิดระบบสุ่มข้อความใส่ท่อนฮุกไหม? (y/n): ").strip().lower()
            use_text = (ask_text == 'y' or ask_text == 'yes')
        
        for i in range(count):
            print(f"\n=======================================")
            print(f"[{shirt_name}] กำลังทำคลิปที่ {i+1}/{count}...")
            
            plan, signature = planner.create_plan(shirt_name, hist_data, user_choice)
            
            if plan is None:
                continue
                
            out_filename, hist_data = history.generate_filename(hist_data, shirt_name)
            hist_data["used_combinations"].append(signature)
            history.save_history(hist_data)
            
            # 🌟 สุ่มข้อความ 1 ประโยค แล้วสร้างรูปภาพ PNG
            text_image_path = None
            if use_text and available_messages:
                selected_msg = random.choice(available_messages)
                print(f"💬 สุ่มได้ข้อความ: {selected_msg}")
                # กำหนดชื่อไฟล์รูปชั่วคราว
                text_image_path = os.path.abspath(f"temp_text_{i}.png")
                create_text_image(selected_msg, FONT_DIR, text_image_path)
            
            # 🌟 ส่ง text_image_path แนบเข้าไปใน builder ด้วย
            builder.build_video(plan, out_filename, use_zoom, use_transition, use_sticker, text_image_path)
            
            # 🌟 ลบไฟล์รูปข้อความทิ้งเมื่อเรนเดอร์เสร็จ จะได้ไม่รกเครื่อง
            if text_image_path and os.path.exists(text_image_path):
                os.remove(text_image_path)
            
    print("\n เสร็จสิ้นกระบวนการทั้งหมด!")

if __name__ == "__main__":
    main()