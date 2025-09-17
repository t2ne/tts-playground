from dotenv import load_dotenv
import os

load_dotenv()

# Sync.so API key
SYNC_API_KEY = os.getenv("SYNCSO")

# Piper TTS voice
PIPER_VOICE = "voices/pt_PT-tuga-medium.onnx"

# Face image/video path
AVATAR_FACE = "photos/face.jpg"  # or .mp4 if you have a neutral video
