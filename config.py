from dotenv import load_dotenv
import os

load_dotenv()

# API key for Sync.so
SYNCSO_API_KEY = os.getenv("SYNCSO")

# Piper TTS voice model
PIPER_VOICE = "voices/pt_PT-tuga-medium.onnx"

# Base avatar video (without speech)
AVATAR_VIDEO = "media/face.mp4"
