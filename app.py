#!/usr/bin/env python
import os

from flask import (
    Flask,
    render_template,
    send_from_directory,
    url_for,
    request,
    jsonify,
    send_file,
    redirect
)
import markdown
from utils.utils import make_image, pages, make_thumbnail
from pathlib import Path
from db import crud
from db.database import SessionLocal
from sqlalchemy.orm import Session
from io import BytesIO
from math import ceil

app = Flask(__name__)

THUMBNAILS  = os.path.join('static', 'thumbnails')

DIR         = os.environ.get('LECTURES_DIR', 'lectures')
LISTEN_HOST = os.environ.get('LISTEN_HOST', '127.0.0.1')
LISTEN_PORT = os.environ.get('LISTEN_PORT', '5000')

app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 60

extensions = ('.pdf', '.md')

if not os.path.exists(DIR):
    os.makedirs(DIR)

if not os.path.exists(THUMBNAILS):
    os.makedirs(THUMBNAILS, exist_ok=True)

files = [f for f in os.listdir(DIR) if f.endswith(extensions)]
files_ = None
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.route('/delete', methods=['POST'])
def delete_file():
    data = request.get_json()

    if not data:
        return jsonify({"error": "No JSON data received"}), 400

    file = data.get('file').split('.')[0]
    file_path = os.path.join(DIR, f"{file}.pdf")
    thum_path = os.path.join(THUMBNAILS, f"{file}.webp")

    if os.path.exists(file_path):
        os.remove(file_path)
        os.remove(thum_path)
        return jsonify({'success': True,
                        'message': 'The file has been successfully deleted.'}), 200
    else:
        return jsonify({'success': False,
                'message': 'File not found.'}), 400


@app.route('/get_files/<int:index>', methods=['POST', 'GET'])
def get_files(index):
    db = next(get_db())

    splitter = 8

    match request.method: 
        case "POST":
            query = request.form.get("query")
            pager = ceil(crud.count_by_name(db, query)/splitter)
            archive = crud.get_by_name(db, 
                                       query,
                                       offset=splitter*(index-1),
                                       limit=splitter)
        case "GET":
            pager = ceil(crud.count_files(db)/splitter)
            archive = crud.get_filenames(db,
                                         offset=splitter*(index-1),
                                         limit=splitter)

    return jsonify({"files" : archive,
                    "pages": pager}), 200

@app.route('/')
def index():
    return render_template('index.html')


@app.route('/thumbnail/<filename>')
def get_thumbnail(filename):
    db = next(get_db())
    print(filename.replace('webp', 'pdf'))
    image = crud.get_thumbnail_by_name(db, filename)
    if image:
        print(f"Image found: {image.filename}")
        return send_file(BytesIO(image.thumbnail_image), mimetype="image/webp")
    else:
        return "Image not found", 404


@app.route('/file/<filename>')
def serve_file(filename):
    db = next(get_db())
    print(filename)
    file = crud.get_file_by_name(db, filename)
    if file:
        print(f"File found: {file.filename}")
        return send_file(BytesIO(file.data), mimetype="application/pdf")
    else:
        return "File not found", 404
    

@app.route('/view_pdf/<filename>')
def view_pdf(filename):
    if filename.endswith('.pdf'):
        page = request.args.get('page', default=1, type=int)
        return render_template(
            'view_pdf.html',
            pdf_url=url_for(
                'serve_file',
                filename=filename),
            page=page)
    return "File not found", 404


@app.route('/view_md/<filename>')
def view_md(filename):
    if filename.endswith('.md'):
        with open(os.path.join(DIR, filename), "r", encoding="utf-8") as f:
            md_content = f.read()

        return render_template(
            'view_md.html',
            md_url=url_for('serve_file', filename=filename),
            content=markdown.markdown(
                md_content,
                extensions=['fenced_code', 'tables'],
                output_format="html5"))
    return "File not found", 404


@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return jsonify({'success': False,
                        'message': 'File not found.'}), 400

    file = request.files['file']

    if not file.filename:
        return jsonify({'success': False,
                        'message': 'Invalid file name.'}), 400

    if not file.filename.endswith(extensions):
        return jsonify({'success': False,
                        'message': 'Only PDF files are allowed.'}), 415

    file_path = os.path.join(DIR, file.filename)
    file.save(file_path)
    make_image(file.filename, DIR, THUMBNAILS, 1)

    return jsonify({'success': True,
                    'message': 'File uploaded successfully.'}), 201


if __name__ == '__main__':
    app.run(host=LISTEN_HOST, port=LISTEN_PORT, debug=True)
