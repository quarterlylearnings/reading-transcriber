from flask import Flask, request, send_file
app = Flask(__name__)

@app.route('/upload', methods=['POST'])
def upload_file():
    file = request.files['file']
    if file:
        return "Audio file received", 200