import vosk, sys, sounddevice as sd, queue, json
from config import VOSK_MODEL_PATH

q = queue.Queue()
model = vosk.Model(VOSK_MODEL_PATH)
samplerate = 16000
device = None

def transcribe():
    rec = vosk.KaldiRecognizer(model, samplerate)
    with sd.RawInputStream(samplerate=samplerate, blocksize=8000,
                           device=device, dtype='int16',
                           channels=1, callback=lambda indata, f, t, s: q.put(bytes(indata))):
        print("Speak now (CTRL+C to stop)...")
        while True:
            data = q.get()
            if rec.AcceptWaveform(data):
                result = json.loads(rec.Result())
                return result.get("text", "")
