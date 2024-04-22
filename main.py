from flask import Flask, request
from google.cloud import storage
from transcribe import transcribe_gcs_audio_file
from create_document import create_word_document
import os

app = Flask(__name__)

storage_client = storage.Client()
bucket_name = os.getenv("GCS_AUDIO_BUCKET_NAME")
bucket = storage_client.bucket(bucket_name)

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

        blob = bucket.blob(filename)
        blob.upload_from_string(file.read(), content_type=file.content_type)

        uri = f"gs://{bucket_name}/{filename}"
        return transcribe_gcs_audio_file(uri, filename)
 
if __name__ == "__main__":
    app.run()