import config
import os

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

def main_menu():
    settings = config.load_settings()
    
    while True:
        clear_screen()
        print("=== ⚙️ เมนูตั้งค่าโปรแกรม Shirt Maker ===")
        print(f"[1] ขนาดวิดีโอ (Resolution) : {settings['resolution']}")
        print(f"[2] ความคมชัดของไฟล์ (CRF)   : {settings['crf']}")
        print(f"[3] ความแรงการซูมสูงสุด       : {int(settings['zoom_max']*100)}%")
        print(f"[4] ความเร็วทรานซิชันเปลี่ยนภาพ : {settings['transition_duration']} วินาที")
        print("------------------------------------------")
        
        choice = input("พิมพ์หมายเลขที่ต้องการเปลี่ยน (หรือพิมพ์ 0 เพื่อออก): ").strip()
        
        if choice == '0':
            print("✅ ออกจากเมนูตั้งค่าเรียบร้อยแล้ว!")
            break
            
        elif choice == '1':
            print("\n--- 📺 ตั้งค่าขนาดวิดีโอ ---")
            print("💡 คำแนะนำ:")
            print("  [a] 720p  : รวดเร็ว ไฟล์เล็ก เหมาะกับ TikTok/Reels ทั่วไป (ค่ามาตรฐาน)")
            print("  [b] 1080p : ชัดกริ๊บ ภาพเนียนตา แต่คอมจะใช้เวลาประมวลผลนานขึ้นและไฟล์ใหญ่")
            ans = input("เลือก (a หรือ b): ").strip().lower()
            if ans == 'a': settings['resolution'] = "720p"
            elif ans == 'b': settings['resolution'] = "1080p"
            
        elif choice == '2':
            print("\n--- 🎞️ ตั้งค่าความคมชัด (CRF) ---")
            print("💡 คำแนะนำ (ตัวเลขยิ่งน้อยยิ่งชัด แต่ไฟล์จะใหญ่):")
            print("  [a] 18 : ชัดสุดยอดระดับ Master (ไฟล์ใหญ่มาก)")
            print("  [b] 23 : มาตรฐาน สมดุลทั้งความชัดและขนาดไฟล์ (แนะนำ)")
            print("  [c] 28 : ชัดน้อยลงมาหน่อย แต่ไฟล์เล็ก ส่งผ่านไลน์ง่าย")
            ans = input("เลือก (a, b หรือ c): ").strip().lower()
            if ans == 'a': settings['crf'] = "18"
            elif ans == 'b': settings['crf'] = "23"
            elif ans == 'c': settings['crf'] = "28"
            
        elif choice == '3':
            print("\n--- 🔍 ตั้งค่าความแรงการซูมสูงสุด ---")
            print("💡 คำแนะนำ:")
            print("  [a] 8% : ซูมน้อยๆ เนียนๆ ไม่เวียนหัว ภาพไม่แตก")
            print("  [b] 15% : ซูมกำลังดี เห็นชัดเจน (แนะนำ)")
            print("  [c] 20% : ซูมแรงสะใจ แต่ถ้าคลิปต้นฉบับไม่ชัด ภาพอาจจะแตกได้")
            ans = input("เลือก (a, b หรือ c): ").strip().lower()
            if ans == 'a': settings['zoom_max'] = 0.08
            elif ans == 'b': settings['zoom_max'] = 0.15
            elif ans == 'c': settings['zoom_max'] = 0.20
            
        elif choice == '4':
            print("\n--- ⏱️ ตั้งค่าความเร็วทรานซิชัน (รอยต่อคลิปฮุก) ---")
            print("💡 คำแนะนำ:")
            print("  [a] 0.2 วินาที : เปลี่ยนภาพไว กระชับทันใจ (แนะนำ)")
            print("  [b] 0.5 วินาที : เปลี่ยนภาพแบบนุ่มนวล")
            print("  [c] 0.8 วินาที : เปลี่ยนภาพช้าๆ ฟีลลิ่งแบบซีนอารมณ์")
            ans = input("เลือก (a, b หรือ c): ").strip().lower()
            if ans == 'a': settings['transition_duration'] = 0.2
            elif ans == 'b': settings['transition_duration'] = 0.5
            elif ans == 'c': settings['transition_duration'] = 0.8

        # บันทึกค่าที่เปลี่ยนใหม่ลงไฟล์ JSON
        config.save_settings(settings)

if __name__ == "__main__":
    main_menu()