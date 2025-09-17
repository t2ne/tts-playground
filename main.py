from modules import stt, tts, lipsync, chatbot

def main():
    # Step 1: Listen to user
    user_text = stt.transcribe()
    print("👤 You said:", user_text)

    # Step 2: Chatbot response
    response_text = chatbot.get_response(user_text)
    print("🤖 Bot:", response_text)

    # Step 3: TTS (Piper)
    audio_file = tts.speak(response_text)

    # Step 4: Lip Sync (Sync.so API)
    lipsync.animate(audio_file)

if __name__ == "__main__":
    main()
