import subprocess
import os
from config import PIPER_VOICE, OUTPUT_DIR

def speak(text, filename="output.wav"):
    os.makedirs(OUTPUT_DIR, exist_ok=True)  # cria a pasta se não existir
    output_file = os.path.join(OUTPUT_DIR, filename)

    # Piper CLI requer -m para o modelo
    cmd = [
        "piper",
        "-m", PIPER_VOICE,
        "-t", text,
        "-f", output_file
    ]
    result = subprocess.run(cmd, capture_output=True)
    if result.returncode != 0:
        raise RuntimeError(f"Piper CLI failed:\n{result.stderr.decode()}")

    if os.path.getsize(output_file) == 0:
        raise RuntimeError("Piper produced empty audio.")

    print(f"Audio generated at {output_file}, size: {os.path.getsize(output_file)} bytes")
    return output_file
