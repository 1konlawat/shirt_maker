import os
import subprocess
import random
import probe
import effects
import config

# --- เริ่ม: ส่วนตั้งค่าระบบสติกเกอร์ ---
def get_random_png(folder_path):
    if not os.path.exists(folder_path):
        return None
    png_files = [file for file in os.listdir(folder_path) if file.lower().endswith('.png')]
    return os.path.join(folder_path, random.choice(png_files)) if png_files else None

sticker_configs = [
    {
        "name": "บนขวา",
        "path": r"C:\Users\KK_KK\OneDrive - Rajamangala University of Technology Phranakhon\เดสก์ท็อป\shirt_maker\sticker\ประกอบ\ขวา",
        "scale": 450,
        "overlay": "W-w+150:-100"
    },
    {
        "name": "ตรงกลาง",
        "path": r"C:\Users\KK_KK\OneDrive - Rajamangala University of Technology Phranakhon\เดสก์ท็อป\shirt_maker\sticker\กลาง",
        "scale": 350,
        "overlay": "(W-w)/2:(H-h)/2"
    },
    {
        "name": "ล่างซ้าย",
        "path": r"C:\Users\KK_KK\OneDrive - Rajamangala University of Technology Phranakhon\เดสก์ท็อป\shirt_maker\sticker\ประกอบ\ซ้าย",
        "scale": 500,
        "overlay": "-200:H-h+100"
    }
]
# --- จบ: ส่วนตั้งค่าระบบสติกเกอร์ ---

def build_video(plan, out_filename, use_zoom, use_transition, use_sticker):
    
    # ลบบรรทัด ask_sticker = input(...) ออกไปเลย
    
    print(f"🔄 กำลังวัดความยาวคลิปทั้ง {len(plan)} คลิป...")
    durations = [probe.get_video_duration(clip) for clip in plan]

    print(f"🔄 กำลังวัดความยาวคลิปทั้ง {len(plan)} คลิป...")
    durations = [probe.get_video_duration(clip) for clip in plan]
    
    print(f"🔄 กำลังคำนวณเอฟเฟกต์...")
    clip_effects = effects.calculate_effects(plan, durations, use_zoom, use_transition)
    
    if not os.path.exists(config.OUTPUT_DIR):
        os.makedirs(config.OUTPUT_DIR)
        
    out_path = os.path.join(os.path.abspath(config.OUTPUT_DIR), out_filename)
    
    inputs = []
    for clip in plan:
        inputs.extend(["-i", os.path.abspath(clip)])
        
    filter_complex = ""
    fps = 30
    
    # 🌟 ดึงค่าขนาดหน้าจอจากระบบ Menu
    if config.SETTINGS.get("resolution") == "1080p":
        w, h = 1080, 1920
    else:
        w, h = 720, 1280
        
    for i in range(len(plan)):
        filter_complex += f"[{i}:a]aformat=sample_rates=44100:channel_layouts=stereo[a{i}];"
        filter_complex += f"[{i}:v]scale={w}:{h}:force_original_aspect_ratio=increase,crop={w}:{h},setsar=1,fps={fps}[v_base{i}];"
        
        if use_zoom:
            eff = clip_effects[i]
            zoom_level = eff["zoom"]
            frames = max(1, int(durations[i] * fps))
            
            if eff["zoom_in"]:
                z_expr = f"1+{zoom_level}*(in/{frames})"
            else:
                z_expr = f"(1+{zoom_level})-{zoom_level}*(in/{frames})"
            
            filter_complex += f"[v_base{i}]zoompan=z='{z_expr}':x='iw/2-(iw/zoom/2)':y='ih/2-(ih/zoom/2)':d=1:s={w}x{h}:fps={fps},unsharp=3:3:0.5[v{i}];"
        else:
            filter_complex += f"[v_base{i}]copy[v{i}];"
            
    # 🌟 ดึงค่าความเร็วทรานซิชันจากระบบ Menu
    trans_dur = config.SETTINGS.get("transition_duration", 0.3)
    concat_v_streams = ""
    concat_a_streams = ""
    concat_count = len(plan)
    
    if use_transition and clip_effects[0]["transition_next"]:
        trans_type = clip_effects[0]["transition_next"]
        if trans_type == "zoom": trans_type = "zoomin"
        
        offset = max(0, durations[0] - trans_dur)
        
        filter_complex += f"[v0][v1]xfade=transition={trans_type}:duration={trans_dur}:offset={offset}[v01];"
        filter_complex += f"[a0][a1]acrossfade=d={trans_dur}[a01];"
        
        concat_v_streams += "[v01]"
        concat_a_streams += "[a01]"
        concat_count = len(plan) - 1 
        
        for i in range(2, len(plan)):
            concat_v_streams += f"[v{i}]"
            concat_a_streams += f"[a{i}]"
            
    else:
        for i in range(len(plan)):
            concat_v_streams += f"[v{i}]"
            concat_a_streams += f"[a{i}]"
            
    # สิ้นสุดการตัดต่อวิดีโอหลัก จะได้ผลลัพธ์เป็น [outv]
    filter_complex += f"{concat_v_streams}concat=n={concat_count}:v=1:a=0[outv];"
    filter_complex += f"{concat_a_streams}concat=n={concat_count}:v=0:a=1[outa]"
    
    final_v_map = "[outv]" # ถ้าไม่มีสติกเกอร์ จะใช้ [outv] ไปแมปออกวิดีโอเลย

    # --- 🌟 ระบบประกอบร่างสติกเกอร์ ---
    if use_sticker:
        valid_stickers = []
        for config_item in sticker_configs:
            file_path = get_random_png(config_item["path"])
            if file_path:
                valid_stickers.append({
                    "name": config_item["name"],
                    "file": file_path,
                    "scale": config_item["scale"],
                    "overlay": config_item["overlay"]
                })

        if valid_stickers:
            print("✅ เปิดระบบสติกเกอร์: พบสติกเกอร์", len(valid_stickers), "ชิ้น")
            
            # เติมตัวสติกเกอร์เข้าไปใน inputs (-i) ต่อจากวิดีโอหลัก
            base_input_index = len(plan)
            
            # ต้องใส่ลูกน้ำ ; ขั้นระหว่าง filter ตัดต่อหลัก กับ filter สติกเกอร์ที่กำลังจะสร้าง
            filter_complex += ";" 
            
            current_stream = "outv" # เริ่มรับภาพที่ตัดต่อเสร็จแล้วจาก [outv] มาเป็นพื้นหลัง
            
            for i, st in enumerate(valid_stickers):
                input_idx = base_input_index + i
                inputs.extend(["-i", st["file"]]) # เอาไฟล์สติกเกอร์ยัดเข้าคำสั่ง
                
                scale_lbl = f"st{i}"
                out_stream = f"ovl{i}"
                
                # 1. ย่อขนาดสติกเกอร์
                filter_complex += f"[{input_idx}:v]scale={st['scale']}:-1[{scale_lbl}];"
                
                # 2. วางทับ
                if i == len(valid_stickers) - 1:
                    # ถ้าเป็นสติกเกอร์ชิ้นสุดท้าย ให้ตั้งชื่อผลลัพธ์ว่า [final_v] เพื่อส่งออก
                    filter_complex += f"[{current_stream}][{scale_lbl}]overlay={st['overlay']}[final_v]"
                    final_v_map = "[final_v]"
                else:
                    # ถ้ายังมีชิ้นอื่นต่อ ให้รันชื่อตัวแปรต่อไปเรื่อยๆ
                    filter_complex += f"[{current_stream}][{scale_lbl}]overlay={st['overlay']}[{out_stream}];"
                    current_stream = out_stream
        else:
            print("❌ ไม่พบไฟล์สติกเกอร์ในโฟลเดอร์ที่กำหนดเลย (ข้ามการแปะสติกเกอร์)")

    # 🌟 ดึงค่าความคมชัด CRF จากระบบ Menu
    crf_val = config.SETTINGS.get("crf", "23")
    
    cmd = [
        "ffmpeg", "-y"
    ] + inputs + [
        "-filter_complex", filter_complex,
        "-map", final_v_map,  # ดึงภาพจาก final_v_map (อาจจะเป็น [outv] หรือ [final_v])
        "-map", "[outa]",     # ดึงเสียงปกติ
        "-c:v", "libx264",
        "-preset", "fast",  
        "-crf", str(crf_val), 
        "-c:a", "aac",
        "-b:a", "128k",
        out_path
    ]
    
    print(f"🚀 กำลังประมวลผลเอฟเฟกต์และเรนเดอร์วิดีโอ...")
    try:
        subprocess.run(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.STDOUT, check=True)
        print(f"✅ สร้างวิดีโอสำเร็จ! ไปดูไฟล์ได้ที่โฟลเดอร์ '{config.OUTPUT_DIR}'")
    except subprocess.CalledProcessError as e:
        print(f"❌ เกิดข้อผิดพลาดในการใส่เอฟเฟกต์! อาจเกิดจากคลิปบางตัวมีปัญหา")