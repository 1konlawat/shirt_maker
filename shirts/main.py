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
    
    # 🌟 เพิ่มคำถามสติกเกอร์ตรงนี้ (ถามแค่ครั้งเดียวก่อนเข้าลูปทำคลิป)
    ask_sticker = input("เอาสติกเกอร์ 3 ตำแหน่งด้วยไหม? (y/n): ").strip().lower()
    use_sticker = (ask_sticker == 'y' or ask_sticker == 'yes')
    
    hist_data = history.load_history()
    
    for order in orders:
        shirt_name = order['shirt']
        count = order['count']
        
        for i in range(count):
            print(f"\n=======================================")
            print(f"[{shirt_name}] กำลังทำคลิปที่ {i+1}/{count}...")
            
            plan, signature = planner.create_plan(shirt_name, hist_data)
            
            if plan is None:
                continue
                
            out_filename, hist_data = history.generate_filename(hist_data, shirt_name)
            
            # บันทึกประวัติ
            hist_data["used_combinations"].append(signature)
            history.save_history(hist_data)
            
            # 🌟 ส่งค่า use_sticker เข้าไปใน builder (อย่าลืมแก้ builder.py ให้รับค่าตัวนี้ด้วยนะครับ)
            builder.build_video(plan, out_filename, use_zoom, use_transition, use_sticker)
            
    print("\n เสร็จสิ้นกระบวนการทั้งหมด!")

if __name__ == "__main__":
    main()