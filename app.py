from flask import (
    Flask,
    request,
    render_template,
    url_for,
    send_file,
    abort,
)
from werkzeug.utils import secure_filename
from io import BytesIO
import logging
import os

import firebase_admin
from firebase_admin import credentials, storage

ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

app = Flask(__name__)

logging.basicConfig(level=logging.INFO)

bucket = None
try:
    cred_path = os.environ.get("GOOGLE_APPLICATION_CREDENTIALS")
    bucket_name = os.environ.get("FIREBASE_STORAGE_BUCKET")
    if cred_path and bucket_name:
        if not firebase_admin._apps:
            cred = credentials.Certificate(cred_path)
            firebase_admin.initialize_app(cred, {"storageBucket": bucket_name})
        bucket = storage.bucket()
    else:
        logging.warning(
            "Firebase credentials or storage bucket not set; file uploads disabled"
        )
except Exception as e:
    logging.error(f"Failed to initialize Firebase: {e}")

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['GET', 'POST'])
def upload_file():
    if bucket is None:
        abort(500, description="Storage not configured")
    if request.method == 'POST':
        if 'file' not in request.files:
            return 'Dosya bulunamadı', 400
        file = request.files['file']
        if file.filename == '':
            return 'Dosya seçilmedi', 400
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            blob = bucket.blob(filename)
            blob.upload_from_file(file, content_type=file.content_type)
            return render_template('success.html')
        else:
            return 'Geçersiz dosya türü', 400
    return render_template('upload.html')


@app.route('/image/<filename>')
def view_image(filename):
    if bucket is None:
        abort(500, description="Storage not configured")
    blob = bucket.blob(filename)
    if not blob.exists():
        abort(404)
    file_stream = BytesIO()
    blob.download_to_file(file_stream)
    file_stream.seek(0)
    return send_file(file_stream, mimetype=blob.content_type)


@app.route('/download/<filename>')
def download_image(filename):
    if bucket is None:
        abort(500, description="Storage not configured")
    blob = bucket.blob(filename)
    if not blob.exists():
        abort(404)
    file_stream = BytesIO()
    blob.download_to_file(file_stream)
    file_stream.seek(0)
    return send_file(
        file_stream,
        mimetype=blob.content_type,
        as_attachment=True,
        download_name=filename,
    )


@app.route('/gallery')
def gallery():
    if bucket is None:
        abort(500, description="Storage not configured")
    blobs = bucket.list_blobs()
    images = [b.name for b in blobs if allowed_file(b.name)]
    return render_template('gallery.html', images=images)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
