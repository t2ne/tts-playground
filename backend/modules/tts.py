import os
import subprocess
from typing import Optional
from config import PIPER_VOICE, OUTPUT_DIR


def speak(text, filename="output.wav", voice_model: Optional[str] = None):
    """Synthesize speech with Piper.

    :param text: Text to speak
    :param filename: Output WAV filename under OUTPUT_DIR
    :param voice_model: Optional override for the Piper model path
    """

    os.makedirs(OUTPUT_DIR, exist_ok=True)
    output_file = os.path.join(OUTPUT_DIR, filename)

    model_path = voice_model or PIPER_VOICE

    cmd = ["piper", "-m", model_path, "-t", text, "-f", output_file]
    result = subprocess.run(cmd, capture_output=True)
    
    if result.returncode != 0:
        raise RuntimeError(f"Piper failed: {result.stderr.decode()}")
    if os.path.getsize(output_file) == 0:
        raise RuntimeError("Empty audio file generated")
    
    print(f"Audio generated at {output_file}, size: {os.path.getsize(output_file)} bytes")
    return output_file
