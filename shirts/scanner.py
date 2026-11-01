import os
import config

def get_valid_shirts():
    """สแกนหาโฟลเดอร์เสื้อผ้าที่มีโฟลเดอร์ย่อยครบตามที่กำหนด"""
    # ถ้ายังไม่มีโฟลเดอร์ shirts ให้สร้างให้เลย
    if not os.path.exists(config.BASE_DIR):
        os.makedirs(config.BASE_DIR)
        print(f"⚠️ เพิ่งสร้างโฟลเดอร์ '{config.BASE_DIR}' กรุณาใส่โฟลเดอร์เสื้อผ้าลงไปก่อน")
        return []

    valid_shirts = []
    
    # อ่านรายชื่อไฟล์/โฟลเดอร์ทั้งหมดใน BASE_DIR
    for item in os.listdir(config.BASE_DIR):
        item_path = os.path.join(config.BASE_DIR, item)
        
        # เช็คว่าเป็น "โฟลเดอร์" เท่านั้น
        if os.path.isdir(item_path):
            has_all_subfolders = True
            for sub in config.SUBFOLDERS:
                if not os.path.exists(os.path.join(item_path, sub)):
                    has_all_subfolders = False
                    break
            
            if has_all_subfolders:
                valid_shirts.append(item)
                
    return sorted(valid_shirts)