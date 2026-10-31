def ask_yes_no(question):
    """ฟังก์ชันถามคำถาม y/n และบังคับให้ตอบถูก"""
    while True:
        ans = input(f"{question} (y/n): ").strip().lower()
        if ans in ['y', 'n']:
            return ans == 'y'
        print("❌ กรุณาพิมพ์ y หรือ n เท่านั้น")

def get_user_orders(valid_shirts):
    """รับคำสั่งทั้งหมดจากผู้ใช้"""
    if not valid_shirts:
        print("❌ ไม่พบโฟลเดอร์เสื้อผ้าที่ถูกต้องเลย (โฟลเดอร์ย่อยอาจไม่ครบ 4 อัน)")
        return None, False, False

    print("\n--- ตั้งค่าเริ่มต้น (ใช้กับทุกคลิปในรอบนี้) ---")
    use_zoom = ask_yes_no("1. เอาซูมไหม?")
    use_transition = ask_yes_no("2. เอาทรานซิชันไหม?")

    orders = []
    
    while True:
        print("\n--- เลือกเสื้อผ้า ---")
        for i, shirt in enumerate(valid_shirts, 1):
            print(f"{i}. {shirt}")
        
        # ถามเลือกเสื้อ
        while True:
            try:
                choice = input(f"เลือกหมายเลขเสื้อผ้า (1-{len(valid_shirts)}): ")
                shirt_idx = int(choice) - 1
                if 0 <= shirt_idx < len(valid_shirts):
                    break
                print(f"❌ กรุณาพิมพ์ตัวเลขระหว่าง 1 ถึง {len(valid_shirts)}")
            except ValueError:
                print("❌ กรุณาพิมพ์เป็นตัวเลขเท่านั้น")
        
        selected_shirt = valid_shirts[shirt_idx]

        # ถามจำนวนคลิป
        while True:
            try:
                choice = input(f"ต้องการทำคลิปของ '{selected_shirt}' จำนวนกี่คลิป?: ")
                num_clips = int(choice)
                if num_clips > 0:
                    break
                print("❌ กรุณาใส่ตัวเลขที่มากกว่า 0")
            except ValueError:
                print("❌ กรุณาพิมพ์เป็นตัวเลขเท่านั้น")
        
        orders.append({
            "shirt": selected_shirt,
            "count": num_clips
        })

        if not ask_yes_no("เอาเสื้อผ้าโฟลเดอร์อื่นเพิ่มอีกไหม?"):
            break
            
    return orders, use_zoom, use_transition