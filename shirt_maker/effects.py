import random

def get_zoom_level(duration):
    if duration <= 1.5:
        return 0.05        # 5%
    elif 1.5 < duration <= 3.0:
        return random.uniform(0.08, 0.10)  # 8-10%
    elif 3.0 < duration <= 5.0:
        return random.uniform(0.10, 0.12)  # 10-12%
    else:
        return random.uniform(0.12, 0.15)  # สูงสุดแค่ 15% พอครับ
    
def calculate_effects(plan, durations, use_zoom, use_transition):
    """วางแผนเอฟเฟกต์ (ซูมและทรานซิชัน) ให้แต่ละคลิป"""
    effects = []
    current_zoom_in = True  # ตัวแปรสลับซูมเข้า/ออก
    
    for i in range(len(plan)):
        clip_eff = {
            "zoom": 0.0,
            "zoom_in": True,
            "transition_next": None # ชนิดทรานซิชันที่จะส่งไปคลิปถัดไป
        }
        
        # 1. คำนวณการซูม
        if use_zoom:
            clip_eff["zoom"] = get_zoom_level(durations[i])
            clip_eff["zoom_in"] = current_zoom_in
            current_zoom_in = not current_zoom_in # สลับทิศทางสำหรับคลิปถัดไป
            
        # 2. คำนวณทรานซิชัน (ใส่เฉพาะรอยต่อคลิปที่ 0 (ฮุก) ไปคลิปที่ 1 (ท่อนโชว์))
        if use_transition and i == 0:
            # ถ้าคลิปสั้นเกิน 1 วินาที ให้ตัดตรงๆ
            if durations[0] < 1.0 or durations[1] < 1.0:
                print("   ⚠️ คลิปฮุกสั้นเกินไป ขอเปลี่ยนเป็นตัดตรงๆ แทนทรานซิชัน")
            else:
                if use_zoom and clip_eff["zoom_in"]:
                    clip_eff["transition_next"] = "zoom"
                else:
                    clip_eff["transition_next"] = random.choice(["fade", "wipeleft", "wiperight"])
                    
        effects.append(clip_eff)
        
    return effects