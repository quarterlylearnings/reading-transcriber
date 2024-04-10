from flask import send_file
from docx import Document

def create_word_document(transcription, filename):
    document = Document()
    document.add_heading("Reading Title", 0)
    document.add_heading("A Commentary", level=2)
    document.add_paragraph(transcription)

    docx_filename = f"{filename}.docx"
    document.save(docx_filename)

    return send_file(docx_filename, as_attachment=True)