# 🌐 TTS Avatar with Lip Sync

A complete text-to-speech system with realistic lip synchronization using AI-powered face animation.

## Features

- **Real-time Speech Recognition** - Vosk
- **Natural Voice Synthesis** - Piper TTS
- **Advanced Lip Synchronization** - Wav2Lip AI
- **Automatic Video Generation** - FFmpeg
- **Intelligent Fallback System** - Works even without AI models
- **100% Local Processing** - No external APIs required

## Setup

```bash
# Clone and setup everything automatically
git clone https://github.com/t2ne/tts-playground.git

cd tts-playground

# Create the venv (only once)
python3 -m venv .venv

# Enter the venv in the terminal every time you want to use the project
source .venv/bin/activate  # Windows: .venv\Scripts\activate

# One-time command setup (installs everything)
python setup.py

# Run the application
python main.py

#To close the venv
deactivate
```

That's it!

Note: you must have the FFmpeg system dependency installed on your machine. More information on how to install it below.

## Project Structure

```
tts-playground/
│
├── main.py
├── config.py
├── requirements.txt
├── setup.py
├── .gitignore
├── README.md
│
├── backend/
│   ├── modules/
│   │   ├── __init__.py
│   │   ├── stt.py
│   │   ├── tts.py
│   │   └── lipsync.py
│   └── extras/
│       ├── models/
│       │   └── vosk-model-small-pt-0.3/
│       ├── photos/
│       │   └── face,jpg
│       ├── voices/
│       │   ├── pt_PT-tugao-medium.onnx
│       │   ├── pt_PT-tugao-medium.onnx.json
│       │   ├── dii_pt-PT.onnx
│       │   └── dii_pt-PT.onnx.json
│       └── Wav2Lip/
│
└── output/
```

## Requirements

**requirements.txt includes (simplified):**

```
python-dotenv
vosk
sounddevice
numpy
piper-tts
ffmpeg-python
torch
torchvision
opencv-python
librosa==0.9.2
tqdm
numba
requests
```

## FFmpeg Dependency

This project requires FFmpeg for video processing and lip-sync video muxing.
You must have FFmpeg installed and available on your PATH:

```bash
# macOS
brew install ffmpeg

# Ubuntu/Debian
sudo apt update && sudo apt install ffmpeg

# Windows
# Download from https://ffmpeg.org/download.html
```

## Download Vosk Model (Done on Setup by Default)

Download the small model and place it under `models/`:

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
OUTPUT_DIR = "output/"

# Two Piper voices installed by setup.py
PIPER_VOICE_MALE = "backend/extras/voices/pt_PT-tugao-medium.onnx"
PIPER_VOICE_FEMALE = "backend/extras/voices/dii_pt-PT.onnx"

AVATAR_FACE = "backend/extras/photos/face.jpg"
VOSK_MODEL_PATH = "backend/extras/models/vosk-model-small-pt-0.3"
```

## Running the Project

```bash
python main.py
```

- When prompted, choose the voice:
  - `1` → Male (Tuga)
  - `2` or Enter → Female (Dii, default)
- Speak into your microphone when prompted.
- Piper generates `output/output.wav` (temporary).
- Wav2Lip (if checkpoint is available) or FFmpeg creates `output/output.mp4` with your avatar and synchronized audio.
- The intermediate WAV file is removed automatically after video creation.

## Notes

- **Fully Local**: No external APIs required - everything runs on your machine.
- **Automatic Fallback**: Uses system FFmpeg if available, otherwise falls back to Python FFmpeg.
- **Portuguese Support**: Optimized for European Portuguese (pt_PT) but can work with other languages.
- **Cross-Platform**: Works on macOS, Linux, and Windows.

## Current Features

- **Advanced Lip Sync**: Real lip-sync animation using Wav2Lip AI technology
- **Fallback System**: Basic video generation if Wav2Lip checkpoint unavailable
- **Single Face**: Works with one face image at a time
- **Portuguese Focus**: Optimized for Portuguese speech recognition and TTS

## Future Enhancements

- Add support for multiple languages
- Multiple face/avatar options
- Web interface for easier use
- Real-time processing capabilities
- GPU acceleration optimization

## Author

- [t2ne](https://github.com/t2ne)

## References

- [Piper TTS](https://github.com/rhasspy/piper)
- [Vosk STT](https://alphacephei.com/vosk/)
- [FFmpeg](https://ffmpeg.org/)
