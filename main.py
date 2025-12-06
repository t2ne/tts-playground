import sys
import argparse
from pathlib import Path

from backend.modules import stt, tts, lipsync

def run_cli():
    """Run the original CLI version"""
    print("Running CLI mode...")
    user_text = stt.transcribe()
    print("You said:", user_text)
    
    audio_file = tts.speak(user_text)
    video_path = lipsync.generate_lipsync(audio_file)
    
    if video_path:
        print(f"Video created: {video_path}")
    else:
        print("Failed to create video")

def run_web():
    """Launch the Gradio web interface"""
    try:
        from frontend.gradio import launch_interface
        print("Starting TTS Avatar Web Interface...")
        launch_interface(share=True, debug=False)
    except ImportError as e:
        print(f"Error importing web interface: {e}")
        sys.exit(1)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="TTS Avatar with Lip Sync")
    parser.add_argument(
        "--cli", 
        action="store_true", 
        help="Run in CLI mode instead of web interface"
    )
    
    args = parser.parse_args()
    
    if args.cli:
        run_cli()
    else:
        run_web()
