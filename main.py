from modules import stt, tts, lipsync

if __name__ == "__main__":
    user_text = stt.transcribe()
    print("You said:", user_text)
    
    audio_file = tts.speak(user_text)
    video_path = lipsync.generate_lipsync(audio_file)
    
    if video_path:
        print(f"✅ Video created: {video_path}")
    else:
        print("❌ Failed to create video")
