from dotenv import load_dotenv
import os

load_dotenv()

OUTPUT_DIR = "output/"

# --- Voice configuration ---
# We install two Piper voices in setup.py:
# 1) Male (Tuga):  backend/extras/voices/pt_PT-tugao-medium.onnx
# 2) Female (Dii): backend/extras/voices/dii_pt-PT.onnx

PIPER_VOICE_MALE = "backend/extras/voices/pt_PT-tugao-medium.onnx"
PIPER_VOICE_FEMALE = "backend/extras/voices/dii_pt-PT.onnx"

# Default voice if nothing else is specified
PIPER_VOICE = PIPER_VOICE_FEMALE

AVATAR_FACE = "backend/extras/photos/face.jpg"

VOSK_MODEL_PATH = "backend/extras/models/vosk-model-small-pt-0.3"
