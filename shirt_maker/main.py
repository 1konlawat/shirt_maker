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
            
            # สั่งประกอบคลิปจริง
            builder.build_video(plan, out_filename, use_zoom, use_transition)
            
    print("\n เสร็จสิ้นกระบวนการทั้งหมด!")

if __name__ == "__main__":
    main()