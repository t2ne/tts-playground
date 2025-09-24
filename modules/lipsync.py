import os
import subprocess
from config import AVATAR_FACE, OUTPUT_DIR

def generate_lipsync(audio_file, face_file=AVATAR_FACE, filename="output.mp4"):
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    output_path = os.path.join(OUTPUT_DIR, filename)
    
    if not os.path.exists(face_file) or not os.path.exists(audio_file):
        print(f"❌ Missing files: {face_file} or {audio_file}")
        return None
    
    print(f"🎬 Creating video: {audio_file} + {face_file} → {output_path}")
    
    cmd = [
        'ffmpeg', '-y', '-loop', '1', '-i', face_file, '-i', audio_file,
        '-vf', 'scale=trunc(iw/2)*2:trunc(ih/2)*2',
        '-c:v', 'libx264', '-tune', 'stillimage', '-c:a', 'aac', '-b:a', '128k',
        '-pix_fmt', 'yuv420p', '-shortest', output_path
    ]
    
    try:
        subprocess.run(cmd, capture_output=True, text=True, check=True)
        print(f"✅ Video created: {output_path}")
        return output_path
    except FileNotFoundError:
        try:
            import imageio_ffmpeg as ffmpeg
            cmd[0] = ffmpeg.get_ffmpeg_exe()
            subprocess.run(cmd, capture_output=True, text=True, check=True)
            print(f"✅ Video created: {output_path}")
            return output_path
        except Exception as e:
            print(f"❌ FFmpeg error: {e}")
            return None
    except subprocess.CalledProcessError as e:
        print(f"❌ FFmpeg failed: {e.stderr}")
        return None