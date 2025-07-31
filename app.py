from flask import Flask, request, render_template_string, redirect, url_for
from werkzeug.utils import secure_filename
import os

UPLOAD_FOLDER = 'uploads'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

os.makedirs(UPLOAD_FOLDER, exist_ok=True)

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

FORM_HTML = """
<!doctype html>
<title>Fotoğraf Yükle</title>
<h1>Fotoğraf Yükle</h1>
<form method=post enctype=multipart/form-data>
  <input type=file name=file>
  <input type=submit value=Yükle>
</form>
"""

SUCCESS_HTML = """
<!doctype html>
<title>Yükleme Başarılı</title>
<h1>Fotoğraf yüklendi!</h1>
<a href="{{ url_for('upload_file') }}">Başka fotoğraf yükle</a>
"""

@app.route('/', methods=['GET'])
def index():
    return redirect(url_for('upload_file'))

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
            return render_template_string(SUCCESS_HTML)
        else:
            return 'Geçersiz dosya türü', 400
    return render_template_string(FORM_HTML)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
