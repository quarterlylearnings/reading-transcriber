from flask import Flask, request, send_file, jsonify
from google.cloud import speech, storage
from docx import Document
import io

app = Flask(__name__)

storage_client = storage.Client()
bucket_name = io.getenv("GCS_AUDIO_BUCKET_NAME")
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

        return jsonify({"message": "File uploaded successfully", "gcs_path": f"gs://{bucket_name}/{filename}"})
        # transcription = transcribe_audio(content)
        # return create_word_document(transcription)
    
#TODO - PLACE IN A SEPARATE FILE (GOING TO GROW DUE TO ADDING CONTEXT)
def transcribe_audio(content, use_uri=False, uri=None):
    client = speech.SpeechClient()

    if use_uri:
        audio = speech.RecognitionAudio(uri=uri)
    else:
        audio = speech.RecognitionAudio(content=content)

    config = speech.RecognitionConfig(
        encoding=speech.RecognitionConfig.AudioEncoding.LINEAR16,
        sample_rate_hertz=44100,
        language_code="en-US",
        enable_automatic_punctuation=True
    )

    operation = client.long_running_recognize(config=config, audio=audio)
    print("Waiting for operation to complete...")

    response = operation.result(timeout=90)

    transcription = ""
    for result in response.results:
        transcription += result.alternatives[0].transcript + "\n"

    return transcription

#TODO - PLACE IN A SEPARATE FILE
def create_word_document(transcription):
    document = Document()
    document.add_heading("Reading Title", 0)
    document.add_heading("A Commentary", level=2)
    document.add_paragraph(transcription)

    document.save("transcription.docx")

    return send_file("transcription.docx", as_attachment=True)


if __name__ == "__main__":
    app.run(debug=True)
