from modules import stt, tts, lipsync
import threading
from http.server import HTTPServer, SimpleHTTPRequestHandler

# Start local HTTP server
def start_http_server():
    server = HTTPServer(('localhost', 8000), SimpleHTTPRequestHandler)
    print("🌐 HTTP server started at http://localhost:8000")
    server.serve_forever()

if __name__ == "__main__":
    threading.Thread(target=start_http_server, daemon=True).start()

    # Step 1: Record & transcribe
    user_text = stt.transcribe()
    print("👤 You said:", user_text)

    # Step 2: Generate TTS audio
    audio_file = tts.speak(user_text)

    # Step 3: Lip sync
    video_url = lipsync.generate_lipsync(audio_file)
    print("🎬 Your lipsynced video is at:", video_url)
