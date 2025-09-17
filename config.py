from dotenv import load_dotenv
import os

load_dotenv()

SYNC_API_KEY = os.getenv("SYNCSO")

OUTPUT_DIR = "output/"

# --- Substitue with your own config, if u want ---

PIPER_VOICE = "voices/pt_PT-tuga-medium.onnx"

AVATAR_FACE = "photos/face.jpg"

VOSK_MODEL_PATH = "models/vosk-model-small-pt-0.3"