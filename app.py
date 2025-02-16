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
from utils.utils import make_image, chunkify
from pathlib import Path

app = Flask(__name__)

FOLDER = os.path.join('lectures')
THUMBNAILS = os.path.join('static', 'thumbnails')

app.config['UPLOAD_FOLDER'] = FOLDER
app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 60

extensions = ('.pdf', '.md')

if not os.path.exists(FOLDER):
    os.makedirs(FOLDER)

if not os.path.exists(THUMBNAILS):
    os.makedirs(THUMBNAILS, exist_ok=True)

files = [f for f in os.listdir(FOLDER) if f.endswith(extensions)]
#files = {i:files[n:3+n] for i,n in enumerate(range(0, len(files), 3))}

@app.route('/get_files/<int:index>', methods=['POST', 'GET'])
def get_files(index):
	splitter = 4
	archive = chunkify(files, splitter)
	if request.method == "POST":
		query = request.form.get("query")
		if query:
			archive = chunkify([f for f in files if query in f], splitter)
			return jsonify({"files":archive.get(index),
							"chunks":len(archive)}), 200
		return jsonify({"files":archive.get(index),
						"chunks":len(archive)}), 200
	return jsonify({"files":archive.get(index),
					"chunks":len(archive)}), 200

@app.route('/')
def index():
    return render_template('index.html')


@app.route('/thumbnail/<filename>')
def get_thumbnail(filename):
    image_path = os.path.join(THUMBNAILS, filename)
    if not os.path.exists(image_path):
        make_image(filename.replace('.webp', '.pdf'), FOLDER, THUMBNAILS, 1)
    return send_file(image_path, mimetype="image/webp")


@app.route('/file/<filename>')
def serve_file(filename):
    return send_from_directory(FOLDER, filename)


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
        with open(os.path.join(FOLDER, filename), "r", encoding="utf-8") as f:
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

    file_path = os.path.join(FOLDER, file.filename)
    file.save(file_path)
    make_image(file.filename, FOLDER, THUMBNAILS, 1)

    return jsonify({'success': True,
                    'message': 'File uploaded successfully.'}), 201


if __name__ == '__main__':
    app.run(host="0.0.0.0", debug=True)
