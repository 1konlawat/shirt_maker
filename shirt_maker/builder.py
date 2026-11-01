import os
import subprocess
import probe
import effects
import config

def build_video(plan, out_filename, use_zoom, use_transition):
    """สั่ง FFmpeg ให้ประกอบคลิปและใส่เอฟเฟกต์ (แก้บัค Zoom ค้าง + ทำภาพให้คมชัดขึ้น)"""
    print(f" กำลังวัดความยาวคลิปทั้ง {len(plan)} คลิป...")
    durations = [probe.get_video_duration(clip) for clip in plan]
    
    print(f" กำลังคำนวณเอฟเฟกต์...")
    clip_effects = effects.calculate_effects(plan, durations, use_zoom, use_transition)
    
    if not os.path.exists(config.OUTPUT_DIR):
        os.makedirs(config.OUTPUT_DIR)
        
    out_path = os.path.join(os.path.abspath(config.OUTPUT_DIR), out_filename)
    
    # 1. เตรียมไฟล์ Input ทั้งหมด
    inputs = []
    for clip in plan:
        inputs.extend(["-i", os.path.abspath(clip)])
        
    filter_complex = ""
    fps = 30
    w = 720
    h = 1280
    
    # 2. ปรับขนาดภาพและใส่ซูม
    for i in range(len(plan)):
        # ปรับเสียงและภาพให้เป็นมาตรฐานเดียวกันก่อน
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
            
            # 🌟 บรรทัดนี้แหละครับที่ใส่ตัวเพิ่มความคมชัด (unsharp=3:3:0.5) ต่อท้าย zoompan ไปแล้ว!
            filter_complex += f"[v_base{i}]zoompan=z='{z_expr}':x='iw/2-(iw/zoom/2)':y='ih/2-(ih/zoom/2)':d=1:s={w}x{h}:fps={fps},unsharp=3:3:0.5[v{i}];"
        else:
            filter_complex += f"[v_base{i}]copy[v{i}];"
            
    # 3. ใส่ทรานซิชัน
    trans_dur = 0.3
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
            
    # 4. ประกอบร่าง (Concat)
    filter_complex += f"{concat_v_streams}concat=n={concat_count}:v=1:a=0[outv];"
    filter_complex += f"{concat_a_streams}concat=n={concat_count}:v=0:a=1[outa]"
    
    cmd = [
        "ffmpeg", "-y"
    ] + inputs + [
        "-filter_complex", filter_complex,
        "-map", "[outv]",
        "-map", "[outa]",
        "-c:v", "libx264",
        "-preset", "fast",  
        "-crf", "23",       
        "-c:a", "aac",
        "-b:a", "128k",
        out_path
    ]
    
    print(f" กำลังประมวลผลเอฟเฟกต์และเรนเดอร์วิดีโอ... (อาจใช้เวลาสักครู่)")
    try:
        subprocess.run(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.STDOUT, check=True)
        print(f" สร้างวิดีโอสำเร็จ! ไปดูไฟล์ได้ที่โฟลเดอร์ '{config.OUTPUT_DIR}'")
    except subprocess.CalledProcessError as e:
        print(f"❌ เกิดข้อผิดพลาดในการใส่เอฟเฟกต์! อาจเกิดจากคลิปบางตัวมีปัญหา")