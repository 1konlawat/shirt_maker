import random
import config

def get_zoom_level(duration):
    """คำนวณซูมตามสัดส่วนของค่าสูงสุดที่ตั้งไว้ใน Menu"""
    # โหลดค่า zoom_max จากระบบ (ถ้าไม่เจอให้ใช้ 0.15)
    max_z = config.SETTINGS.get("zoom_max", 0.15)
    
    if duration <= 1.5:
        return max_z * 0.33       # คลิปสั้น ซูมแค่ 33% ของค่า Max
    elif 1.5 < duration <= 3.0:
        return random.uniform(max_z * 0.50, max_z * 0.66)
    elif 3.0 < duration <= 5.0:
        return random.uniform(max_z * 0.66, max_z * 0.80)
    else:
        return random.uniform(max_z * 0.80, max_z) # คลิปยาว ซูมจัดเต็มถึง Max

def calculate_effects(plan, durations, use_zoom, use_transition):
    effects = []
    current_zoom_in = True
    
    for i in range(len(plan)):
        clip_eff = {
            "zoom": 0.0,
            "zoom_in": True,
            "transition_next": None
        }
        
        if use_zoom:
            clip_eff["zoom"] = get_zoom_level(durations[i])
            clip_eff["zoom_in"] = current_zoom_in
            current_zoom_in = not current_zoom_in
            
        if use_transition and i == 0:
            if durations[0] < 1.0 or durations[1] < 1.0:
                print("   ⚠️ คลิปฮุกสั้นเกินไป ขอเปลี่ยนเป็นตัดตรงๆ แทนทรานซิชัน")
            else:
                if use_zoom and clip_eff["zoom_in"]:
                    clip_eff["transition_next"] = "zoom"
                else:
                    clip_eff["transition_next"] = random.choice(["fade", "wipeleft", "wiperight"])
                    
        effects.append(clip_eff)
        
    return effects