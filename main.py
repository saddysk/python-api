from flask import Flask, request, jsonify
from dotenv import load_dotenv
from services.trim_audio import trim_and_upload_mp3

load_dotenv()

app = Flask(__name__)

@app.route('/', methods=['GET'])
def home():
    return 'WAGMI!'

# TODO: improve the code to accept audio in .mp3 file format as well
@app.route('/mp3/trim_and_upload', methods=['POST'])
def api_trim_and_upload():
    data = request.json
    url = data.get('url')
    start_time_ms = data.get('start')
    end_time_ms = data.get('end')
    file_name = data.get('fileName')

    if not all([url, start_time_ms, end_time_ms, file_name]):
        return jsonify({"status": "error", "message": "All fields (url, start, end, file_name) are required!"}), 400

    # Convert start and end times to integers (assuming they're sent as strings)
    try:
        start_time_ms = int(start_time_ms)
        end_time_ms = int(end_time_ms)
    except ValueError:
        return jsonify({"status": "error", "message": "Start and End times should be valid integers!"}), 400

    # Call the function and get the resulting URL
    trimmed_audio_url = trim_and_upload_mp3(url, start_time_ms, end_time_ms, file_name)

    # Return the resulting URL in the response
    response_data = {
        "status": 'success',
        "code": 200,
        "data": trimmed_audio_url
    }

    return jsonify(response_data), 200


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5002)