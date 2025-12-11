import json
import queue
import sounddevice as sd
import vosk
from config import VOSK_MODEL_PATH

q = queue.Queue()
model = vosk.Model(VOSK_MODEL_PATH)

def transcribe():
    rec = vosk.KaldiRecognizer(model, 16000)
    with sd.RawInputStream(samplerate=16000, blocksize=8000, dtype='int16',
                           channels=1, callback=lambda indata, f, t, s: q.put(bytes(indata))):
        print("Speak now (CTRL+C to stop)...")
        while True:
            data = q.get()
            if rec.AcceptWaveform(data):
                result = json.loads(rec.Result())
                text = result.get("text", "")
                if text:
                    return text
                else:
                    print("Didn't catch that, try again...")
