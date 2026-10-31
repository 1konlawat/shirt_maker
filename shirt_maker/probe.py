import subprocess

def get_video_duration(filepath):
    """หาความยาวของคลิปเป็นวินาทีด้วย ffprobe"""
    cmd = [
        'ffprobe', '-v', 'error', 
        '-show_entries', 'format=duration',
        '-of', 'default=noprint_wrappers=1:nokey=1', 
        filepath
    ]
    try:
        # สั่งรัน ffprobe ซ่อนหน้าต่าง
        result = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True)
        return float(result.stdout.strip())
    except Exception as e:
        print(f" วัดความยาวคลิปไม่ได้ ({filepath}): {e}")
        return 0.0