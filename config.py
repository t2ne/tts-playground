from dotenv import load_dotenv
import os

load_dotenv()

OUTPUT_DIR = "output/"

# --- Substitue with your own config, if u want ---

PIPER_VOICE = "backend/extras/voices/pt_PT-tuga-medium.onnx"

AVATAR_FACE = "frontend/media/photos/face.jpg"

VOSK_MODEL_PATH = "backend/extras/models/vosk-model-small-pt-0.3"
