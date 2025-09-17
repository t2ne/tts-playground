import vosk, sys, sounddevice as sd, queue, json

q = queue.Queue()
model = vosk.Model("vosk-model-small-pt-0.3")  # Portuguese model
samplerate = 16000
device = None

def callback(indata, frames, time, status):
    if status:
        print(status, file=sys.stderr)
    q.put(bytes(indata))

def transcribe():
    rec = vosk.KaldiRecognizer(model, samplerate)
    with sd.RawInputStream(samplerate=samplerate, blocksize=8000,
                           device=device, dtype='int16',
                           channels=1, callback=callback):
        print("🎤 Fala agora (CTRL+C para parar)...")
        while True:
            data = q.get()
            if rec.AcceptWaveform(data):
                result = json.loads(rec.Result())
                return result.get("text", "")
