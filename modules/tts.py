from piper import PiperVoice
from config import PIPER_VOICE

voice = PiperVoice.load(PIPER_VOICE)

def speak(text, output_file="output.wav"):
    with open(output_file, "wb") as f:
        voice.synthesize(text, f)
    return output_file
