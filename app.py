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
    redirect,
    Response
)
import markdown
from utils.utils import make_image, pages, make_thumbnail
from pathlib import Path
from io import BytesIO
from math import ceil
from models import crud, SessionLocal

app = Flask(__name__)

THUMBNAILS_DIR = os.path.join('static', 'thumbnails')

APP_HOST = os.environ.get('APP_HOST', '127.0.0.1')
APP_PORT = os.environ.get('APP_PORT', '5000')

app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 60
app.config['SERVER_NAME'] = f"{APP_HOST}:{APP_PORT}"

os.makedirs(THUMBNAILS_DIR, exist_ok=True)
extensions = ('.pdf', '.md')

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

db = next(get_db())


print("[+] Dumping thumbnails images...")
for image, filename in crud.get_all_images(db):
    if image is None:
        print(f"[-] {filename} image not found... skiping...")
        continue
        
    if os.path.exists(f"{THUMBNAILS_DIR}/{filename}"):
        continue

    #static/thumbnails/ or maybe else where...
    with open(os.path.join(THUMBNAILS_DIR, filename.replace('pdf', 'webp')), "wb") as f:
        f.write(image)

print("[+] Dumping thumbnails complete!")


@app.route('/get_files/<int:index>', methods=['POST', 'GET'])
def get_files(index):
    db = next(get_db())

    splitter = 8

    match request.method:
        case "POST":
            # This retrieves all the necessary files from the database based on the query
            query = request.form.get("query")
            pager = ceil(crud.count_by_name(db, query)/splitter)
            archive = crud.get_by_name(db,
                                       query,
                                       offset=splitter*(index-1),
                                       limit=splitter)
        case "GET":
            # This retrieves all the necessary files from the database
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
    if os.path.exists(f"{THUMBNAILS_DIR}/{filename}"):
        return send_from_directory(THUMBNAILS_DIR, filename)

    db = next(get_db())
    thumbnail = crud.get_thumbnail_by_name(db,
                                           filename)

    if not thumbnail:
        return "File not found", 404

    with open(os.path.join(THUMBNAILS_DIR, filename), "wb") as f:
        f.write(thumbnail)

    return send_from_directory(THUMBNAILS_DIR, filename)

@app.route('/file/<filename>')
def serve_file(filename):
    db = next(get_db())
    file = crud.get_file_by_name(db, filename).file
    if file:
        print(f"File found: {filename}")
        return Response(file, mimetype="application/pdf")
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
        db = next(get_db())
        print(filename)
        file = crud.get_file_by_name(db, filename).file
        return render_template(
            'view_md.html',
            md_url=url_for('serve_file', filename=filename),
            content=markdown.markdown(
                file.decode("utf-8"),
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

    #file_path = os.path.join(DIR, file.filename)
    #file.save(file_path)
    #make_image(file.filename, DIR, THUMBNAILS, 1)

    return jsonify({'success': True,
                    'message': 'File uploaded successfully.'}), 201


if __name__ == '__main__':
    app.run(debug=True)
