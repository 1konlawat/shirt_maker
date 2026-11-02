import scanner
import prompts
import history
import planner
import builder

def main():
    print("=== เริ่มโปรแกรม Shirt Maker ===")
    
    valid_shirts = scanner.get_valid_shirts()
    result = prompts.get_user_orders(valid_shirts)
    
    if result[0] is None:
        return
        
    orders, use_zoom, use_transition = result
    
    # คำถามสติกเกอร์
    ask_sticker = input("เอาสติกเกอร์ 3 ตำแหน่งด้วยไหม? (y/n): ").strip().lower()
    use_sticker = (ask_sticker == 'y' or ask_sticker == 'yes')
    
    # 🌟 1. เพิ่มคำถามเรื่องโหมดการนำเสนอตรงนี้ (ถามครั้งเดียวก่อนเข้าลูป)
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
        
        for i in range(count):
            print(f"\n=======================================")
            print(f"[{shirt_name}] กำลังทำคลิปที่ {i+1}/{count}...")
            
            # 🌟 2. ส่งค่า user_choice เข้าไปใน planner.create_plan
            plan, signature = planner.create_plan(shirt_name, hist_data, user_choice)
            
            if plan is None:
                continue
                
            out_filename, hist_data = history.generate_filename(hist_data, shirt_name)
            
            # บันทึกประวัติ
            hist_data["used_combinations"].append(signature)
            history.save_history(hist_data)
            
            # ส่งค่า use_sticker เข้าไปใน builder 
            builder.build_video(plan, out_filename, use_zoom, use_transition, use_sticker)
            
    print("\n เสร็จสิ้นกระบวนการทั้งหมด!")

if __name__ == "__main__":
    main()