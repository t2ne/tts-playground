from piper import PiperVoice
import numpy as np
import soundfile as sf
import os
from config import PIPER_VOICE

voice = PiperVoice.load(PIPER_VOICE)

def speak(text, output_file="output.wav"):
    audio_gen = voice.synthesize(text)

    # Ensure generator produces audio
    audio_list = []
    try:
        for chunk in audio_gen:
            if chunk is not None:
                audio_list.append(chunk)
    except Exception as e:
        raise RuntimeError(f"Piper synthesis failed: {e}")

    if not audio_list:
        raise RuntimeError("⚠️ Piper did not produce any audio. Check your voice model or OS compatibility.")

    audio_array = np.concatenate(audio_list)
    audio_int16 = np.int16(audio_array * 32767)

    sf.write(output_file, audio_int16, voice.sample_rate, subtype='PCM_16')
    print(f"✅ Audio generated at {output_file}, size: {os.path.getsize(output_file)} bytes")
    return output_file
