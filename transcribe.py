from flask import jsonify
from google.cloud import speech
import os


def transcribe_gcs_audio_file(gcs_uri, filename):
    client = speech.SpeechClient()

    audio = speech.RecognitionAudio(uri=gcs_uri)

    speaker_diarization_config = speech.SpeakerDiarizationConfig(
        enable_speaker_diarization=True,
        min_speaker_count=1,
        max_speaker_count=4,
    )

    config = speech.RecognitionConfig(
        encoding=speech.RecognitionConfig.AudioEncoding.LINEAR16,
        sample_rate_hertz=16000,
        language_code="en-US",
        enable_automatic_punctuation=True,
        diarization_config=speaker_diarization_config,
    )

    output_config = speech.TranscriptOutputConfig(
        gcs_uri=f"gs://{os.getenv('GCS_TRANSCRIPTION_BUCKET_NAME')}/{filename}.json"
    )

    request = speech.LongRunningRecognizeRequest(
        config=config, audio=audio, output_config=output_config
    )

    operation = client.long_running_recognize(request=request)
    print("Waiting for operation to complete...")

    #return a JSON object with a boolean of whether the operation is running
    response = jsonify({"running": operation.running()})
    return response
