from flask import (
    Flask,
    request,
    render_template,
    redirect,
    url_for,
    send_from_directory,
)
from werkzeug.utils import secure_filename
import os
import tempfile
import firebase_admin
from firebase_admin import credentials, storage as fb_storage

UPLOAD_FOLDER = os.path.join(tempfile.gettempdir(), 'uploads')
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

os.makedirs(UPLOAD_FOLDER, exist_ok=True)

FIREBASE_BUCKET = os.environ.get("FIREBASE_BUCKET")
firebase_bucket = None
if FIREBASE_BUCKET:
    cred_path = os.environ.get("GOOGLE_APPLICATION_CREDENTIALS")
    try:
        if cred_path and os.path.exists(cred_path):
            cred = credentials.Certificate(cred_path)
            firebase_admin.initialize_app(cred, {"storageBucket": FIREBASE_BUCKET})
        else:
            firebase_admin.initialize_app(options={"storageBucket": FIREBASE_BUCKET})
        firebase_bucket = fb_storage.bucket()
    except Exception:
        firebase_bucket = None

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
            path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(path)
            if firebase_bucket:
                blob = firebase_bucket.blob(filename)
                blob.upload_from_filename(path)
                try:
                    blob.make_public()
                except Exception:
                    pass
            return render_template('success.html')
        else:
            return 'Geçersiz dosya türü', 400
    return render_template('upload.html')


@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)


@app.route('/gallery')
def gallery():
    if firebase_bucket:
        blobs = firebase_bucket.list_blobs()
        images = [blob.public_url for blob in blobs if allowed_file(blob.name)]
        return render_template('gallery.html', images=images, hosted=True)
    else:
        images = [f for f in os.listdir(app.config['UPLOAD_FOLDER']) if allowed_file(f)]
        return render_template('gallery.html', images=images, hosted=False)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
