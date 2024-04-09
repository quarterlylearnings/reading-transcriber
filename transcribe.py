from google.cloud import speech
import os

def transcribe_gcs_audio_file(gcs_uri, filename):
    client = speech.SpeechClient()
    
    audio = speech.RecognitionAudio(uri=gcs_uri)
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