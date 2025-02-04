#!/usr/bin/env python
from flask import Flask, render_template, send_from_directory, url_for, request
import os

app = Flask(__name__)

PDF_FOLDER = os.path.join('lectures')
app.config['UPLOAD_FOLDER'] = PDF_FOLDER
#app.config["TEMPLATES_AUTO_RELOAD"] = True
#app.config["SEND_FILE_MAX_AGE_DEFAULT"] = 0

if not os.path.exists(PDF_FOLDER):
    os.makedirs(PDF_FOLDER)

@app.route('/')
def index():
    pdf_files = [f for f in os.listdir(PDF_FOLDER) if f.endswith('.pdf')]
    return render_template('index.html', pdf_files=pdf_files)

@app.route('/pdf/<filename>')
def serve_pdf(filename):
    return send_from_directory(PDF_FOLDER, filename)

@app.route('/view/<filename>')
def view_pdf(filename):
    page = request.args.get('page', default = 1, type = int)
    return render_template('view_pdf.html', pdf_url=url_for('serve_pdf', filename=filename), page=page)

@app.route('/upload', methods=['POST'])
def upload_file():

    if 'file' not in request.files:
        return {'success': False, 'message': 'No se encontró el archivo'}

    file = request.files['file']
    if file.filename == '' and file.filename is None:
        return {'success': False, 'message': 'Nombre de archivo inválido'}

    if file and file.filename.endswith('.pdf'):
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], file.filename))
        return {'success': True, 'message': 'Archivo subido correctamente'}
    else:
        return {'success': False, 'message': 'Solo se permiten archivos PDF'}

if __name__ == '__main__':
    app.run(host="0.0.0.0", debug=True)
