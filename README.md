# Audio Transcription Tool

This is a web application written to accept an audio files, transcribe it using Google's Speech-to-Text API, and generate a downloadable Word document containing the transcription. It leverages Flask for the web server, Google Cloud Storage for storing audio files, and will soon use Google Cloud Firestore for managing metadata.

<!-- ## Architecture Overview

The application architecture is structured to handle audio file uploads, process them for transcription, and manage both the files and their transcription metadata. -->


### Key Components

- **Flask Web Server**: Manages file uploads and serves the generated Word documents.
- **Google Cloud Storage (GCS)**: Stores the uploaded audio files.
- **Google Speech-to-Text API**: Performs the audio file transcriptions.
- **python-docx**: Generates Word documents from the transcription texts.
<!-- - [FUTURE] **Google Cloud Firestore**: Keeps metadata about the audio files and their transcription statuses. -->

## Setup and Deployment

### Prerequisites

- Python 3.8 or later.
- A Google Cloud account.
- Flask installed in your Python environment.
- Google Cloud SDK installed for deployment purposes. [not necessary for running locally]

### Local Development Setup

1. **Clone this repository**:
   ```bash
   git clone git@github.com:quarterlylearnings/reading-transcriber.git
   cd reading-transcriber
   ``````

2. **Install dependencies**:
    ```bash
    pip install -r requirements.txt
    ```

3. **Configure [Google Cloud service account](https://cloud.google.com/iam/docs/best-practices-for-managing-service-account-keys) authentication**:

    Set the `GOOGLE_APPLICATION_CREDENTIALS` environment variable to the path of your Google Cloud service account key file.

    ```bash
    export GOOGLE_APPLICATION_CREDENTIALS="/path/to/your/service-account-file.json"
    ```

4. **Run the application**:

    ```bash
    flask run
    ```
