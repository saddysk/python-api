import io
import base64
from pydub import AudioSegment
import urllib.request

def trim_and_upload_mp3(input_source, start_time_ms, end_time_ms):
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

    # convert to base64
    base64_encoded_audio = base64.b64encode(buffer.getvalue()).decode('utf-8')

    return base64_encoded_audio
