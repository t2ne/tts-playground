import os
import sys
import subprocess
import cv2
import numpy as np
from config import AVATAR_FACE, OUTPUT_DIR

# Add Wav2Lip to path
WAV2LIP_PATH = os.path.join(os.path.dirname(__file__), '..', 'extras', 'Wav2Lip')
sys.path.append(WAV2LIP_PATH)

def generate_lipsync_wav2lip(audio_file, face_file=AVATAR_FACE, filename="output.mp4"):
    """
    Generate lip-synced video using Wav2Lip
    """
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    output_path = os.path.join(OUTPUT_DIR, filename)
    
    if not os.path.exists(face_file) or not os.path.exists(audio_file):
        print(f"❌ Missing files: {face_file} or {audio_file}")
        return None
    
    checkpoint_path = os.path.join(WAV2LIP_PATH, 'checkpoints', 'wav2lip_gan.pth')
    
    if not os.path.exists(checkpoint_path):
        print(f"Wav2Lip checkpoint not found at {checkpoint_path}")
        print("Please download it manually from:")
        print("https://iiitaphyd-my.sharepoint.com/personal/radrabha_m_research_iiit_ac_in/_layouts/15/download.aspx?share=Eb3LEzbfuKlJiR600lQWRxgBIY27JZdq8B7fuee9ew2Dug")
        print("Falling back to basic video generation...")
        return generate_lipsync_basic(audio_file, face_file, filename)
    
    print(f"Creating Wav2Lip video: {audio_file} + {face_file} → {output_path}")
    
    try:
        # Convert to absolute paths for Wav2Lip
        face_abs = os.path.abspath(face_file)
        audio_abs = os.path.abspath(audio_file)
        output_abs = os.path.abspath(output_path)
        
        # Run Wav2Lip inference
        cmd = [
            'python', os.path.join(WAV2LIP_PATH, 'inference.py'),
            '--checkpoint_path', checkpoint_path,
            '--face', face_abs,
            '--audio', audio_abs,
            '--outfile', output_abs
        ]
        
        result = subprocess.run(cmd, capture_output=True, text=True, cwd=WAV2LIP_PATH)
        
        if result.returncode == 0 and os.path.exists(output_path):
            print(f"✅ Wav2Lip video created: {output_path}")
            return output_path
        else:
            print(f"Wav2Lip failed: {result.stderr}")
            print("Falling back to basic video generation...")
            return generate_lipsync_basic(audio_file, face_file, filename)
            
    except Exception as e:
        print(f"Wav2Lip error: {e}")
        print("Falling back to basic video generation...")
        return generate_lipsync_basic(audio_file, face_file, filename)

def generate_lipsync_basic(audio_file, face_file=AVATAR_FACE, filename="output.mp4"):
    """
    Fallback: Generate basic video with static image and audio
    """
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    output_path = os.path.join(OUTPUT_DIR, filename)
    
    print(f"Creating basic video: {audio_file} + {face_file} → {output_path}")
    
    cmd = [
        'ffmpeg', '-y', '-loop', '1', '-i', face_file, '-i', audio_file,
        '-vf', 'scale=trunc(iw/2)*2:trunc(ih/2)*2',
        '-c:v', 'libx264', '-tune', 'stillimage', '-c:a', 'aac', '-b:a', '128k',
        '-pix_fmt', 'yuv420p', '-shortest', output_path
    ]

    try:
        subprocess.run(cmd, capture_output=True, text=True, check=True)
        print(f"✅ Basic video created: {output_path}")
        return output_path
    except FileNotFoundError:
        print("❌ FFmpeg not found. Please install ffmpeg and ensure it is in your PATH.")
        return None
    except subprocess.CalledProcessError as e:
        print(f"❌ FFmpeg failed: {e.stderr}")
        return None

def generate_lipsync(audio_file, face_file=AVATAR_FACE, filename="output.mp4"):
    """
    Main function: Try Wav2Lip first, fallback to basic if needed
    """
    return generate_lipsync_wav2lip(audio_file, face_file, filename)