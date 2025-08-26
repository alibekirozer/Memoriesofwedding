from flask import (
    Flask,
    request,
    render_template,
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

UPLOAD_FOLDER = os.path.join('static', 'uploads')
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

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
            "Firebase credentials or storage bucket not set; using local storage"
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
    if request.method == 'POST':
        if 'file' not in request.files:
            return 'Dosya bulunamadı', 400
        file = request.files['file']
        if file.filename == '':
            return 'Dosya seçilmedi', 400
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            if bucket:
                blob = bucket.blob(filename)
                blob.upload_from_file(file, content_type=file.content_type)
            else:
                file.save(os.path.join(UPLOAD_FOLDER, filename))
            return render_template('success.html')
        else:
            return 'Geçersiz dosya türü', 400
    return render_template('upload.html')


@app.route('/image/<filename>')
def view_image(filename):
    if bucket:
        blob = bucket.blob(filename)
        if not blob.exists():
            abort(404)
        file_stream = BytesIO()
        blob.download_to_file(file_stream)
        file_stream.seek(0)
        return send_file(file_stream, mimetype=blob.content_type)
    file_path = os.path.join(UPLOAD_FOLDER, filename)
    if not os.path.exists(file_path):
        abort(404)
    return send_file(file_path)


@app.route('/download/<filename>')
def download_image(filename):
    if bucket:
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
    file_path = os.path.join(UPLOAD_FOLDER, filename)
    if not os.path.exists(file_path):
        abort(404)
    return send_file(
        file_path,
        as_attachment=True,
        download_name=filename,
    )


@app.route('/gallery')
def gallery():
    if bucket:
        blobs = bucket.list_blobs()
        images = [b.name for b in blobs if allowed_file(b.name)]
    else:
        images = [f for f in os.listdir(UPLOAD_FOLDER) if allowed_file(f)]
    return render_template('gallery.html', images=images)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
