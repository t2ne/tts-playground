import time
from sync import Sync
from sync.common import Audio, GenerationOptions, Video
from sync.core.api_error import ApiError
from config import SYNCSO_API_KEY, AVATAR_VIDEO

client = Sync(
    base_url="https://api.sync.so",
    api_key=SYNCSO_API_KEY
).generations

def animate(audio_file, output_name="avatar_talking"):
    try:
        response = client.create(
            input=[Video(url=AVATAR_VIDEO), Audio(url=audio_file)],
            model="lipsync-2",
            options=GenerationOptions(sync_mode="cut_off"),
            outputFileName=output_name
        )
    except ApiError as e:
        print(f'❌ Request failed: {e.status_code} {e.body}')
        return None

    job_id = response.id
    print(f"✅ Job submitted: {job_id}")

    generation = client.get(job_id)
    status = generation.status
    while status not in ['COMPLETED', 'FAILED']:
        print(f"⏳ Polling status for job {job_id}...")
        time.sleep(10)
        generation = client.get(job_id)
        status = generation.status

    if status == 'COMPLETED':
        print(f"🎬 Done! Output URL: {generation.output_url}")
        return generation.output_url
    else:
        print(f"❌ Generation {job_id} failed")
        return None
