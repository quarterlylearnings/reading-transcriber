from flask import Flask, request
from google.cloud import storage
from transcribe import transcribe_gcs_audio_file
from create_document import create_word_document
import os

app = Flask(__name__)

storage_client = storage.Client()
bucket_name = os.getenv("GCS_AUDIO_BUCKET_NAME")
bucket = storage_client.bucket(bucket_name)

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

        blob = bucket.blob(filename)
        blob.upload_from_string(file.read(), content_type=file.content_type)

        uri = f"gs://{bucket_name}/{filename}"
        transcription = transcribe_gcs_audio_file(uri, filename)
        return create_word_document(transcription, filename)
 

