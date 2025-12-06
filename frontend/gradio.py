import gradio as gr
import os
import sys
from pathlib import Path

# Add parent directory to path to import backend modules
sys.path.append(str(Path(__file__).parent.parent))

from backend.modules import stt, tts, lipsync
from config import OUTPUT_DIR, AVATAR_FACE

def process_text_to_video(input_text):
    """Complete pipeline: Text -> Audio -> Video with lip sync"""
    if not input_text or input_text.strip() == "":
        return None, "Please enter some text to convert to speech."
    
    try:
        # Generate audio from text
        audio_file = tts.speak(input_text.strip())
        
        if not audio_file or not os.path.exists(audio_file):
            return None, "Failed to generate audio file."
        
        # Generate lip-synced video
        video_path = lipsync.generate_lipsync(audio_file)
        
        if video_path and os.path.exists(video_path):
            return video_path, f"✅ Video created successfully!\nAudio: {audio_file}\nVideo: {video_path}"
        else:
            return None, "❌ Failed to create lip-synced video."
            
    except Exception as e:
        return None, f"❌ Error in processing: {str(e)}"

def process_audio_to_video(audio_file):
    """Process uploaded audio file to create lip-sync video"""
    if audio_file is None:
        return None, "Please upload an audio file."
    
    try:
        # Generate lip-synced video from uploaded audio
        video_path = lipsync.generate_lipsync(audio_file)
        
        if video_path and os.path.exists(video_path):
            return video_path, f"✅ Video created from uploaded audio!\nVideo: {video_path}"
        else:
            return None, "❌ Failed to create lip-synced video from audio."
            
    except Exception as e:
        return None, f"❌ Error processing audio: {str(e)}"

# Create a simple interface without complex components
def create_interface():
    with gr.Blocks(title="TTS Avatar") as demo:
        gr.HTML("<h1 style='text-align: center;'>🌐 TTS Avatar with Lip Sync</h1>")
        
        with gr.Row():
            with gr.Column():
                gr.HTML("<h3>📝 Text to Video</h3>")
                text_input = gr.Textbox(
                    label="Enter text to speak",
                    placeholder="Type your message here...",
                    lines=3
                )
                text_button = gr.Button("Generate Video from Text")
                
            with gr.Column():
                gr.HTML("<h3>🎵 Audio to Video</h3>")
                audio_input = gr.File(label="Upload Audio File", file_types=['audio'])
                audio_button = gr.Button("Generate Video from Audio")
        
        with gr.Row():
            with gr.Column():
                video_output = gr.Video(label="Generated Video")
            with gr.Column():
                status_output = gr.Textbox(label="Status", lines=6)
        
        # Event handlers
        text_button.click(
            fn=process_text_to_video,
            inputs=text_input,
            outputs=[video_output, status_output]
        )
        
        audio_button.click(
            fn=process_audio_to_video,
            inputs=audio_input,
            outputs=[video_output, status_output]
        )
    
    return demo

def launch_interface(share=False, debug=False):
    """Launch the Gradio interface"""
    print("🚀 Starting TTS Avatar Web Interface...")
    demo = create_interface()
    return demo.launch(share=share, debug=debug, server_name="0.0.0.0", server_port=7860)

def main():
    """Main function to launch the web interface"""
    launch_interface(share=False, debug=False)

if __name__ == "__main__":
    main()
