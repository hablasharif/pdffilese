from flask import Flask, render_template, request, redirect, url_for, send_file
from PyPDF2 import PdfMerger, PdfFileReader
import os
from io import BytesIO

app = Flask(__name__)

# Set the upload folder and allowed file extensions
app.config['UPLOAD_FOLDER'] = 'uploads'
app.config['ALLOWED_EXTENSIONS'] = {'pdf'}

# Function to check if a filename has an allowed extension
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in app.config['ALLOWED_EXTENSIONS']

# Route to display the upload form
@app.route('/')
def index():
    return render_template('index.html')

# Route to handle file upload and merging
@app.route('/merge', methods=['POST'])
def merge_pdf():
    # Check if the POST request has the file parts
    if 'files[]' not in request.files:
        return redirect(request.url)

    files = request.files.getlist('files[]')

    # Check if the files have valid extensions
    for file in files:
        if not (file and allowed_file(file.filename)):
            return "Invalid file format. Please upload PDF files."

    # Create a folder for uploaded files if it doesn't exist
    if not os.path.exists(app.config['UPLOAD_FOLDER']):
        os.makedirs(app.config['UPLOAD_FOLDER'])

    # Save the uploaded files and merge them
    pdf_merger = PdfMerger()
    for file in files:
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
        file.save(file_path)
        pdf_merger.append(file_path)

    # Merge the PDF files
    merged_pdf = BytesIO()
    pdf_merger.write(merged_pdf)
    pdf_merger.close()

    # Display the merged PDF in the web page
    merged_pdf.seek(0)
    return send_file(
        BytesIO(merged_pdf.read()),
        mimetype='application/pdf'
    )

if __name__ == '__main__':
    app.run(debug=True)
