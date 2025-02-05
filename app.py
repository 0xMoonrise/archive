#!/usr/bin/env python
import os

from flask import Flask, render_template,\
    send_from_directory, url_for, request, jsonify
# from utils.utils import is_valid_file_ext

app = Flask(__name__)

PDF_FOLDER = os.path.join('lectures')
app.config['UPLOAD_FOLDER'] = PDF_FOLDER
# app.config["TEMPLATES_AUTO_RELOAD"] = True
# app.config["SEND_FILE_MAX_AGE_DEFAULT"] = 0

if not os.path.exists(PDF_FOLDER):
    os.makedirs(PDF_FOLDER)


@app.route('/')
def index():
    extensions = ('.pdf', '.md')
    pdf_files = [f for f in os.listdir(PDF_FOLDER) if f.endswith(extensions)]
    return render_template('index.html', pdf_files=pdf_files)


@app.route('/pdf/<filename>')
def serve_pdf(filename):
    return send_from_directory(PDF_FOLDER, filename)


@app.route('/view/<filename>')
def view_pdf(filename):
    page = request.args.get('page', default=1, type=int)
    return render_template('view_pdf.html',
                           pdf_url=url_for('serve_pdf',
                                           filename=filename), page=page)


@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return jsonify({'success': False,
                        'message': 'File not found.'}), 400

    file = request.files['file']

    if not file.filename:
        return jsonify({'success': False,
                        'message': 'Invalid file name.'}), 400

    if file.filename.endswith('.pdf'):
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
        file.save(file_path)
        return jsonify({'success': True,
                        'message': 'File uploaded successfully.',
                        'path': file_path}), 201

    return jsonify({'success': False,
                    'message': 'Only PDF files are allowed.'}), 415


if __name__ == '__main__':
    app.run(host="0.0.0.0", debug=True)
