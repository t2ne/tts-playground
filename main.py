from modules import stt, tts, lipsync
import os
import threading
from http.server import HTTPServer, SimpleHTTPRequestHandler

# Start a simple HTTP server to serve local files for Sync.so
def start_http_server():
    server = HTTPServer(('localhost', 8000), SimpleHTTPRequestHandler)
    print("🌐 HTTP server started at http://localhost:8000")
    server.serve_forever()

if __name__ == "__main__":
    # Start HTTP server in a background thread
    threading.Thread(target=start_http_server, daemon=True).start()

    # Step 1: Record & transcribe speech
    user_text = stt.transcribe()
    print("👤 You said:", user_text)

    # Step 2: TTS with Piper
    audio_file = tts.speak(user_text)

    # Step 3: Lip sync
    video_url = lipsync.generate_lipsync(audio_file)
    print("🎬 Your lipsynced video is at:", video_url)
