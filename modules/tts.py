import subprocess
import os
from config import PIPER_VOICE

def speak(text, output_file="output.wav"):
    # Piper CLI requires -m for model path
    cmd = [
        "piper",
        "-m", PIPER_VOICE,      # <- model path
        "-t", text,             # <- text to speak
        "-f", output_file        # <- output WAV file
    ]
    result = subprocess.run(cmd, capture_output=True)
    if result.returncode != 0:
        raise RuntimeError(f"Piper CLI failed:\n{result.stderr.decode()}")

    if os.path.getsize(output_file) == 0:
        raise RuntimeError("⚠️ Piper produced empty audio.")

    print(f"Audio generated at {output_file}, size: {os.path.getsize(output_file)} bytes")
    return output_file
