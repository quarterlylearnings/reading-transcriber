from flask import Flask, request
from google.cloud import storage
from transcribe import transcribe_gcs_audio_file
import os
from pydub import AudioSegment

app = Flask(__name__)

storage_client = storage.Client()
bucket_name = os.getenv("GCS_AUDIO_BUCKET_NAME")
bucket = storage_client.bucket(bucket_name)

def convert_mp3_to_wav(mp3_path, wav_path):
    audio = AudioSegment.from_mp3(mp3_path)
    audio.export(wav_path, format="wav")

# Return page describing the upload service and how to use it
@app.route("/")
def root():
    return """
    <h1>Upload an audio file</h1>
    <form method="post" action="/upload" enctype="multipart/form-data">
        <input type="file" name="file">
        <input type="submit" value="Upload">
    </form>
    """

# This route will be used to upload an audio file to the server
@app.route("/upload", methods=["POST"])
def upload_file():
    print(request.files)
    if "file" not in request.files:
        return "No file part", 400
    file = request.files["file"]

    if file.filename == "":
        return "No selected file", 400

    if file:
        filename = file.filename

        file_path = os.path.join("/tmp", filename)
        file.save(file_path)

        if filename.lower.endswith(".mp3"):
            wav_filename = filename.replace(".mp3", ".wav")
            wav_path = os.path.join("/tmp", wav_filename)
            convert_mp3_to_wav(file_path, wav_path)
            file_path = wav_path

        blob = bucket.blob(filename)
        blob.upload_from_filename(file_path)

        uri = f"gs://{bucket_name}/{filename}"
        return transcribe_gcs_audio_file(uri, filename)
 
if __name__ == "__main__":
    app.run()