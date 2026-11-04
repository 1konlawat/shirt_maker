import os
import subprocess
import random
import probe
import effects
import config

# --- ส่วนตั้งค่าสติกเกอร์ (คงเดิม) ---
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

# 🌟 เพิ่มรับค่า text_image_path เข้ามาที่นี่
def build_video(plan, out_filename, use_zoom, use_transition, use_sticker, text_image_path=None):
    
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
        
    # 🌟 ถ้าระบบส่งไฟล์รูปข้อความมา ให้โหลดเข้าเป็น Input ต่อจากวิดีโอหลัก
    text_input_idx = -1
    if text_image_path:
        inputs.extend(["-i", text_image_path])
        text_input_idx = len(plan) # บันทึกเลขลำดับช่องทางของไฟล์ข้อความ
        
    filter_complex = ""
    fps = 60  
    
    if config.SETTINGS.get("resolution") == "1080p":
        w, h = 1080, 1920
    else:
        w, h = 720, 1280
        
    for i in range(len(plan)):
        filter_complex += f"[{i}:a]aformat=sample_rates=44100:channel_layouts=stereo[a{i}];"
        filter_complex += f"[{i}:v]scale={w}:{h}:force_original_aspect_ratio=increase,crop={w}:{h},setsar=1,fps={fps}[v_base{i}];"
        
        # จัดการเรื่อง Zoom
        if use_zoom:
            eff = clip_effects[i]
            zoom_level = eff["zoom"]
            frames = max(1, int(durations[i] * fps))
            
            if eff["zoom_in"]:
                z_expr = f"1+{zoom_level}*(in/{frames})"
            else:
                z_expr = f"(1+{zoom_level})-{zoom_level}*(in/{frames})"
            
            filter_complex += f"[v_base{i}]zoompan=z='{z_expr}':x='iw/2-(iw/zoom/2)':y='ih/2-(ih/zoom/2)':d=1:s={w}x{h}:fps={fps},unsharp=3:3:0.5[v_eff{i}];"
        else:
            filter_complex += f"[v_base{i}]copy[v_eff{i}];"
            
        # 🌟 จัดการเอาข้อความวางทับ เฉพาะคลิปฮุก (i == 0)
        if i == 0 and text_image_path:
            # วางทับด้วยภาพโปร่งใสเต็มจอที่สร้างจาก text_maker.py
            filter_complex += f"[{text_input_idx}:v]scale={w}:{h}[txt_scaled];"
            filter_complex += f"[v_eff0][txt_scaled]overlay=0:0[v0];"
        else:
            # ส่วนคลิปที่ 2 เป็นต้นไป ก็ปล่อยรันปกติ ไม่มีการวางข้อความ
            filter_complex += f"[v_eff{i}]copy[v{i}];"
            
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
            
    filter_complex += f"{concat_v_streams}concat=n={concat_count}:v=1:a=0[outv];"
    filter_complex += f"{concat_a_streams}concat=n={concat_count}:v=0:a=1[outa]"
    
    final_v_map = "[outv]" 

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
            
            # 🌟 ปรับฐานการนับ Index ของสติกเกอร์ (ชดเชยหากมีไฟล์ข้อความแทรกเข้ามาใน Inputs)
            base_input_index = len(plan)
            if text_image_path:
                base_input_index += 1
                
            filter_complex += ";" 
            current_stream = "outv" 
            
            for i, st in enumerate(valid_stickers):
                input_idx = base_input_index + i
                inputs.extend(["-i", st["file"]]) 
                
                scale_lbl = f"st{i}"
                out_stream = f"ovl{i}"
                
                filter_complex += f"[{input_idx}:v]scale={st['scale']}:-1[{scale_lbl}];"
                
                if i == len(valid_stickers) - 1:
                    filter_complex += f"[{current_stream}][{scale_lbl}]overlay={st['overlay']}[final_v]"
                    final_v_map = "[final_v]"
                else:
                    filter_complex += f"[{current_stream}][{scale_lbl}]overlay={st['overlay']}[{out_stream}];"
                    current_stream = out_stream
        else:
            print("❌ ไม่พบไฟล์สติกเกอร์ในโฟลเดอร์ที่กำหนดเลย (ข้ามการแปะสติกเกอร์)")

    crf_val = config.SETTINGS.get("crf", "23")
    
    cmd = [
        "ffmpeg", "-y"
    ] + inputs + [
        "-filter_complex", filter_complex,
        "-map", final_v_map, 
        "-map", "[outa]",    
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