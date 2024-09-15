from flask import Flask, request, render_template
import os

app = Flask(__name__)

# Define your virus signatures here. Each signature is a byte sequence.
virus_database = {
    'virus1': b'\x90\x90\x90',  # Example signature
    'virus2': b'\x4D\x5A\x90',  # Another example
    # Add up to 10 signatures
}

def read_pdf(file):
    """
    Reads the content of a PDF file in binary mode.
    :param file: File object
    :return: Binary content of the file
    """
    return file.read()

def detect_viruses(pdf_content, database):
    """
    Detects viruses in the PDF content based on the provided virus signatures.
    :param pdf_content: Binary content of the PDF file
    :param database: Dictionary of virus signatures
    :return: List of detected virus names
    """
    detections = []
    for name, signature in database.items():
        if signature in pdf_content:
            detections.append(name)
    return detections

@app.route('/', methods=['GET', 'POST'])
def index():
    result = None
    if request.method == 'POST':
        if 'file' not in request.files:
            result = "No file part"
        else:
            file = request.files['file']
            if file.filename == '':
                result = "No selected file"
            elif file and file.filename.endswith('.pdf'):
                pdf_content = read_pdf(file)
                detections = detect_viruses(pdf_content, virus_database)
                if detections:
                    result = f"Virus detected! Names: {', '.join(detections)}"
                else:
                    result = "No virus detected."
            else:
                result = "Invalid file type"
    return render_template('index.html', result=result)

if __name__ == "__main__":
    app.run(debug=True)