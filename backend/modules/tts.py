import os
import subprocess
from config import PIPER_VOICE, OUTPUT_DIR

def speak(text, filename="output.wav"):
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    output_file = os.path.join(OUTPUT_DIR, filename)
    
    cmd = ["piper", "-m", PIPER_VOICE, "-t", text, "-f", output_file]
    result = subprocess.run(cmd, capture_output=True)
    
    if result.returncode != 0:
        raise RuntimeError(f"Piper failed: {result.stderr.decode()}")
    if os.path.getsize(output_file) == 0:
        raise RuntimeError("Empty audio file generated")
    
    print(f"Audio generated at {output_file}, size: {os.path.getsize(output_file)} bytes")
    return output_file
