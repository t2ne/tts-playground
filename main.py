import os
import shutil
from backend.modules import stt, tts, lipsync
from config import PIPER_VOICE_MALE, PIPER_VOICE_FEMALE, OUTPUT_DIR


def main():
    """Run the CLI version by default."""
    print("Running CLI mode...")

    # Clear previous outputs on each run
    if os.path.isdir(OUTPUT_DIR):
        for name in os.listdir(OUTPUT_DIR):
            path = os.path.join(OUTPUT_DIR, name)
            if os.path.isfile(path) or os.path.islink(path):
                os.remove(path)
            elif os.path.isdir(path):
                shutil.rmtree(path)
    
    # Choose voice: 1 = male (Tuga), 2 = female (Dii, default)
    print("Select voice:")
    print("  1) Male (Tuga)")
    print("  2) Female (Dii) [default]")
    choice = input("Voice (1/2): ").strip()

    if choice == "1":
        voice_model = PIPER_VOICE_MALE
        print("Using male voice (Tuga)")
    else:
        voice_model = PIPER_VOICE_FEMALE
        print("Using female voice (Dii)")
    user_text = stt.transcribe()
    print("You said:", user_text)

    audio_file = tts.speak(user_text, voice_model=voice_model)
    video_path = lipsync.generate_lipsync(audio_file)

    if video_path:
        print(f"Video created: {video_path}")
        # Remove intermediate audio file
        try:
            if os.path.exists(audio_file):
                os.remove(audio_file)
        except OSError:
            pass
    else:
        print("Failed to create video")


if __name__ == "__main__":
    main()
