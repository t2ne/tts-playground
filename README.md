# TTS + Lipsync Avatar Project

## Overview
This project creates a talking avatar from a single face image using:
- **Vosk** for speech-to-text (STT)
- **Piper** for text-to-speech (TTS)
- **Sync.so API** for lipsync video generation

The workflow:
1. User speaks into the microphone.
2. Vosk transcribes speech to text.
3. Piper generates a WAV audio file.
4. Sync.so generates a lipsynced MP4 video of the avatar.


## Project Structure
```
tts-playground/
│
├── main.py
├── config.py      
├── requirements.txt  
├── .gitignore
│
├── modules/
│   ├── stt.py
│   ├── tts.py      
│   └── lipsync.py
│
├── media/
│   ├── photos/  
│   │   └── face.jpg
│   └── voices/
│       ├── sample/
│       │   └── speaker_0.mp
│       ├── pt_PT-tuga-medium.onnx
│       └── pt_PT-tuga-medium.onnx.json
│
└── .env
```


## Requirements
```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

**Requirements.txt should include:**
```
vosk
piper-tts
syncsdk
numpy
soundfile
sounddevice
requests
```

## Download Vosk Model
Download the Portuguese small model and place it under `models/`:
```bash
# Using wget
wget https://alphacephei.com/vosk/models/vosk-model-small-pt-0.3.zip

# Or using curl
curl -O https://alphacephei.com/vosk/models/vosk-model-small-pt-0.3.zip

unzip vosk-model-small-pt-0.3.zip -d models/
```

## Configuration
Edit `config.py`:
```python
PIPER_VOICE = 'voices/pt_PT-tuga-medium.onnx'
AVATAR_FACE = 'media/face.jpg'
VOSK_MODEL_PATH = "models/vosk-model-small-pt-0.3"
```

Add `.env`:
```python
SYNCSO=your_api_key
```

## Running the Project
```bash
python main.py
```
- Speak into your microphone.
- Piper generates `output.wav`.
- Sync.so generates `output.mp4` with your avatar talking.


## Notes
- Only the lipsync part requires the audio and face to be uploaded via Sync.so.
- The rest of the pipeline (Vosk + Piper) works locally.
- Ensure your Sync.so API key is valid.

## References
- [Piper TTS](https://github.com/rhasspy/piper)
- [Vosk STT](https://alphacephei.com/vosk/)
- [Sync.so API](https://sync.so)