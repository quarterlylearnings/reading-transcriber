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
        encoding=speech.RecognitionConfig.AudioEncoding.MP3,
        language_code="en-US",
        enable_automatic_punctuation=True,
        diarization_config=speaker_diarization_config,
    )

    operation = client.long_running_recognize(config=config, audio=audio)
    print("Waiting for operation to complete...")

    return operation.running()