import time
from sync import Sync
from sync.common import Audio, GenerationOptions, Video
from sync.core.api_error import ApiError
from config import SYNC_API_KEY, AVATAR_FACE, OUTPUT_DIR
import os
import requests  # necessário para baixar o vídeo

client = Sync(
    base_url="https://api.sync.so",
    api_key=SYNC_API_KEY
).generations

def generate_lipsync(audio_file, face_file=AVATAR_FACE, filename="output.mp4"):
    # cria a pasta OUTPUT_DIR se não existir
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    output_path = os.path.join(OUTPUT_DIR, filename)

    # URLs locais para teste (ou podes fazer upload para Sync.so)
    audio_url = f"http://localhost:8000/{audio_file}"
    video_url = f"http://localhost:8000/{face_file}"

    print("Starting lip sync generation job...")
    try:
        response = client.create(
            input=[Video(url=video_url), Audio(url=audio_url)],
            model="lipsync-2",
            options=GenerationOptions(sync_mode="cut_off")
        )
    except ApiError as e:
        print(f"Request failed: {e.status_code}, {e.body}")
        return None

    job_id = response.id
    print(f"Generation submitted successfully, job id: {job_id}")

    generation = client.get(job_id)
    status = generation.status
    while status not in ["COMPLETED", "FAILED"]:
        print(f"Polling status for job {job_id}...")
        time.sleep(10)
        generation = client.get(job_id)
        status = generation.status

    if status == "COMPLETED":
        # baixa o vídeo para OUTPUT_DIR
        r = requests.get(generation.output_url)
        with open(output_path, "wb") as f:
            f.write(r.content)
        print(f"✅ Lipsynced video saved at {output_path}")
        return output_path
    else:
        print(f"❌ Generation failed for job {job_id}")
        return None
