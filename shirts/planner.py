import os
import random
import config

def get_video_files(folder_path):
    """อ่านรายชื่อไฟล์วิดีโอในโฟลเดอร์"""
    if not os.path.exists(folder_path):
        return []
    valid_exts = ['.mp4', '.mov', '.avi']
    return [f for f in os.listdir(folder_path) if os.path.splitext(f)[1].lower() in valid_exts]

# 🌟 1. เพิ่ม user_mode ตรงบรรทัดนี้
def create_plan(shirt_name, current_history, user_mode):
    """จัดเรียงคลิปตามโหมดที่ผู้ใช้เลือกและเลี่ยงประวัติเดิม"""
    shirt_dir = os.path.join(config.BASE_DIR, shirt_name)
    
    hook_dir = os.path.join(shirt_dir, config.SUBFOLDERS[0])
    normal_dir = os.path.join(shirt_dir, config.SUBFOLDERS[1])
    fast_dir = os.path.join(shirt_dir, config.SUBFOLDERS[2])
    outro_dir = os.path.join(shirt_dir, config.SUBFOLDERS[3])
    
    hook_files = get_video_files(hook_dir)
    normal_files = get_video_files(normal_dir)
    fast_files = get_video_files(fast_dir)
    outro_files = get_video_files(outro_dir)
    
    if not hook_files or not outro_files:
        print(f"⚠️ ข้ามเสื้อ '{shirt_name}' -> มีคลิป 'ฮุก' หรือ 'ปิดท้าย' ไม่พอ!")
        return None, None

    for _ in range(50):
        hook_clip = os.path.join(hook_dir, random.choice(hook_files))
        outro_clip = os.path.join(outro_dir, random.choice(outro_files))
        
        # 🌟 2. เปลี่ยนจากการสุ่ม ให้มาใช้ค่าโหมดที่ผู้ใช้เป็นคนเลือก
        mode = user_mode 
        show_clips = []
        
        if mode == 1: 
            count = min(random.randint(8, 10), len(normal_files))
            if count > 0:
                picked = random.sample(normal_files, count)
                show_clips = [os.path.join(normal_dir, f) for f in picked]
                
        elif mode == 2: 
            count = min(random.randint(11, 18), len(fast_files))
            if count > 0:
                picked = random.sample(fast_files, count)
                show_clips = [os.path.join(fast_dir, f) for f in picked]
                
        else: 
            c_normal = min(random.randint(2, 5), len(normal_files))
            c_fast = min(random.randint(4, 7), len(fast_files))
            
            picked_n = [os.path.join(normal_dir, f) for f in random.sample(normal_files, c_normal)] if c_normal > 0 else []
            picked_f = [os.path.join(fast_dir, f) for f in random.sample(fast_files, c_fast)] if c_fast > 0 else []
            
            mixed = picked_n + picked_f
            random.shuffle(mixed)
            show_clips = mixed
            
        if not show_clips:
            continue
            
        final_plan = [hook_clip] + show_clips + [outro_clip]
        plan_signature = str(final_plan)
        
        if plan_signature not in current_history["used_combinations"]:
            return final_plan, plan_signature
            
    print(f"⚠️ ข้ามเสื้อ '{shirt_name}' -> คลิปในโฟลเดอร์อาจจะน้อยไป สุ่มยังไงก็ซ้ำของเดิม")
    return None, None