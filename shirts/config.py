import os
import json

BASE_DIR = "shirts"
OUTPUT_DIR = "outputs"
SUBFOLDERS = ["ฮุก", "โชว์แบบธรรมดา", "โชว์แบบเร็ว", "ปิดท้าย"]

SETTINGS_FILE = "settings.json"

# ค่ามาตรฐาน (เผื่อเปิดใช้ครั้งแรก)
DEFAULT_SETTINGS = {
    "resolution": "720p",
    "crf": "23",
    "zoom_max": 0.15,
    "transition_duration": 0.3
}

def load_settings():
    """อ่านค่าตั้งค่าจากไฟล์ JSON ถ้าไม่มีให้สร้างใหม่"""
    if not os.path.exists(SETTINGS_FILE):
        save_settings(DEFAULT_SETTINGS)
        return DEFAULT_SETTINGS
    with open(SETTINGS_FILE, 'r', encoding='utf-8') as f:
        return json.load(f)

def save_settings(settings):
    """บันทึกค่าลงไฟล์ JSON"""
    with open(SETTINGS_FILE, 'w', encoding='utf-8') as f:
        json.dump(settings, f, indent=4)

# โหลดการตั้งค่าเตรียมไว้ให้ไฟล์อื่นๆ เรียกใช้ได้ทันที
SETTINGS = load_settings()