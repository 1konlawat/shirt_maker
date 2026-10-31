import json
import os

HISTORY_FILE = "history.json"

def load_history():
    """โหลดประวัติการสร้างคลิปจากไฟล์"""
    if os.path.exists(HISTORY_FILE):
        with open(HISTORY_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)
    
    return {
        "global_count": 0,           # จำนวนคลิปที่ผลิตมาทั้งหมด
        "shirt_counts": {},          # จำนวนคลิปแยกตามเสื้อแต่ละตัว
        "used_combinations": []      # เก็บชุดคลิปที่เคยใช้ไปแล้ว
    }

def save_history(history):
    """บันทึกประวัติกลับลงไปในไฟล์ .json"""
    with open(HISTORY_FILE, 'w', encoding='utf-8') as f:
        json.dump(history, f, ensure_ascii=False, indent=4)

def generate_filename(history, shirt_name):
    """สร้างชื่อไฟล์: ชื่อโฟลเดอร์_จำนวนคลิปในโฟลเดอร์นั้น_จำนวนรวมทุกโฟลเดอร์"""
    history["global_count"] += 1
    global_num = history["global_count"]
    
    if shirt_name not in history["shirt_counts"]:
        history["shirt_counts"][shirt_name] = 0
    history["shirt_counts"][shirt_name] += 1
    shirt_num = history["shirt_counts"][shirt_name]
    
    filename = f"{shirt_name}_{shirt_num}_{global_num}.mp4"
    return filename, history