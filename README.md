# 🎭 Portuguese TTS Avatar with Lip Sync

A complete Portuguese text-to-speech system with realistic lip synchronization using AI-powered face animation.

## ✨ Features

- 🎤 **Real-time Speech Recognition** (Portuguese) - Vosk
- 🗣️ **Natural Voice Synthesis** (Portuguese) - Piper TTS
- 🎭 **Advanced Lip Synchronization** - Wav2Lip AI
- 🎬 **Automatic Video Generation** - FFmpeg
- 🔄 **Intelligent Fallback System** - Works even without AI models
- 🌐 **100% Local Processing** - No external APIs required

## 🚀 Quick Setup

```bash
# Clone and setup everything automatically
git clone https://github.com/t2ne/tts-playground.git

cd tts-playground

# Do to create the venv (only once)
python3 -m venv venv

# Do this to enter the venv in the terminal everytime u want to use the project
source venv/bin/activate  # Windows: venv\Scripts\activate

# One-time command setup (installs everything)
python setup.py

# Run the application
python main.py

#To close the venv
deactivate
```

That's it! 🎉

It is noted that you still need to have the ffmpeg dependency on your machine. More information on how to install it below.

## Project Structure

```
tts-playground/
│
├── main.py
├── config.py
├── requirements.txt
├── .gitignore
├── README.md
│
├── modules/
│   ├── stt.py
│   ├── tts.py
│   └── lipsync.py
│
└── media/
    ├── photos/
    │   └── face.jpg
    └── voices/
        ├── sample/
        │   └── speaker_0.mp
        ├── pt_PT-tuga-medium.onnx
        └── pt_PT-tuga-medium.onnx.json
```

## Requirements

**Requirements.txt includes:**

```
python-dotenv
vosk
sounddevice
numpy
piper-tts
imageio-ffmpeg
torch
torchvision
opencv-python
librosa==0.9.2
tqdm
numba
requests
```

## FFmpeg Dependency

This project requires FFmpeg for video processing. You have two options:

### Option 1: System FFmpeg (Recommended - Faster)

```bash
# macOS
brew install ffmpeg

# Ubuntu/Debian
sudo apt update && sudo apt install ffmpeg

# Windows
# Download from https://ffmpeg.org/download.html
```

### Option 2: Python FFmpeg (Automatic Fallback)

If system FFmpeg is not available, the project automatically uses `imageio-ffmpeg` (included in requirements.txt).
This works out-of-the-box but may be slower for large files.

## Download Vosk Model (Done on Setup by Default)

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
PIPER_VOICE = 'media/voices/pt_PT-tuga-medium.onnx'
AVATAR_FACE = 'media/photos/face.jpg'
VOSK_MODEL_PATH = "models/vosk-model-small-pt-0.3"
OUTPUT_DIR = "output"
```

## Running the Project

```bash
python main.py
```

- Speak into your microphone when prompted.
- Piper generates `output/output.wav`.
- FFmpeg creates `output/output.mp4` with your avatar and synchronized audio.

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

## References

- [Piper TTS](https://github.com/rhasspy/piper)
- [Vosk STT](https://alphacephei.com/vosk/)
- [FFmpeg](https://ffmpeg.org/)
