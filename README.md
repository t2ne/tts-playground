# TTS + Lipsync Avatar Project

## Overview

This project creates a talking avatar from a single face image using:

- **Vosk** for speech-to-text (STT)
- **Piper** for text-to-speech (TTS)
- **FFmpeg** for video generation with audio sync

The workflow:

1. User speaks into the microphone.
2. Vosk transcribes speech to text.
3. Piper generates a WAV audio file.
4. FFmpeg creates an MP4 video combining the face image with the audio.

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

```bash
# To create (first time only)
python3 -m venv venv

# Returning
source venv/bin/activate

#Install requirements
pip install -r requirements.txt

#Quit the venv
deactivate
```

**Requirements.txt includes:**

```
python-dotenv
vosk
sounddevice
numpy
piper-tts
imageio-ffmpeg
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

## Current Limitations

- **Basic Video**: Currently creates a static image video with audio. True lip-sync animation is not yet implemented.
- **Single Face**: Works with one face image at a time.
- **Portuguese Focus**: Optimized for Portuguese speech recognition and TTS.

## Future Enhancements

- Implement real lip-sync animation using Wav2Lip or similar technologies
- Add support for multiple languages
- Web interface for easier use
- Real-time processing capabilities

## References

- [Piper TTS](https://github.com/rhasspy/piper)
- [Vosk STT](https://alphacephei.com/vosk/)
- [FFmpeg](https://ffmpeg.org/)
