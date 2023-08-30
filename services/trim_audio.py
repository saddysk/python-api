import os
import io
from pydub import AudioSegment
from supabase import create_client
import urllib.request

# Initialize Supabase client
BUCKET: str = os.environ.get('SUPABASE_BUCKET')
URL: str = os.environ.get('SUPABASE_URL')
KEY: str = os.environ.get('SUPABASE_SERVICE_ROLE_KEY')

print("SUPABASE_URL:", os.environ.get('SUPABASE_URL'))

supabase = create_client(URL, KEY)

def trim_and_upload_mp3(input_source, start_time_ms, end_time_ms, file_name):
    """Trim an MP3 file and upload the trimmed audio to Supabase without saving it locally."""
    
    # Determine the input source type (URL or local path)
    if input_source.startswith(("http://", "https://")):
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }
        req = urllib.request.Request(input_source, headers=headers)
        
        with urllib.request.urlopen(req) as response:
            audio_data = response.read()
            # Use BytesIO to convert bytes to a file-like object so pydub can process it
            audio = AudioSegment.from_file(io.BytesIO(audio_data), format="mp3")
    else:
        # Load the audio file from local path
        audio = AudioSegment.from_file(input_source, format="mp3")
    
    # Trim the audio
    trimmed_audio = audio[start_time_ms:end_time_ms]
    
    # Save the trimmed audio to a byte stream (in-memory)
    buffer = io.BytesIO()
    trimmed_audio.export(buffer, format="mp3")
    raw_byte_data = buffer.getvalue()
    
    # Upload the trimmed audio to Supabase
    response = supabase.storage.from_(BUCKET).upload(file_name, raw_byte_data)
    
    # Check if upload was successful
    if response.status_code == 200:
        print("Audio uploaded successfully!")
        
        file_path = response.json()
        return file_path.get('Key')
    else:
        print("Failed to upload audio:", response.json())
        return response.json()
