import time
from sync import Sync
from sync.common import Audio, GenerationOptions, Video
from sync.core.api_error import ApiError
from config import SYNC_API_KEY, AVATAR_FACE

client = Sync(
    base_url="https://api.sync.so",
    api_key=SYNC_API_KEY
).generations

def generate_lipsync(audio_file, face_file=AVATAR_FACE):
    # Make sure both files are accessible via HTTP
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
        print(f"✅ Video completed: {generation.output_url}")
        return generation.output_url
    else:
        print(f"❌ Generation failed for job {job_id}")
        return None
