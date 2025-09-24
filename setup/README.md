# Setup Scripts

This folder contains the complete setup automation for the TTS project.

## Quick Setup

```bash
# Complete setup (recommended)
python setup/setup.py

# Just install requirements
python setup/setup.py --requirements-only

# Just setup Wav2Lip
python setup/setup.py --wav2lip-only

# Verify current setup
python setup/setup.py --verify
```

## What the setup does:

1. ✅ **Installs Python requirements** from requirements.txt
2. ✅ **Clones Wav2Lip repository**
3. ✅ **Fixes librosa compatibility** issues
4. ✅ **Downloads Vosk Portuguese model**
5. ✅ **Sets up checkpoint directory** with instructions
6. ✅ **Installs additional dependencies** (face-recognition, dlib)
7. ✅ **Verifies complete setup**

## Manual steps still needed:

After running setup, you still need to:

- 📥 **Download wav2lip_gan.pth** (~400MB) to `Wav2Lip/checkpoints/`
- 📸 **Add your face photo** to `media/photos/face.jpg`

Then you're ready to run: `python main.py` 🚀
