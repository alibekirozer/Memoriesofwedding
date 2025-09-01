from flask import (
    Flask,
    request,
    render_template,
    send_file,
    abort,
)
from werkzeug.utils import secure_filename
import os
import uuid

ALLOWED_EXTENSIONS = {"png", "jpg", "jpeg", "gif"}

app = Flask(__name__)

# Determine a writable upload directory. Vercel provides only ``/tmp`` for
# write access, so use that when the ``VERCEL`` env var is set; otherwise keep
# uploads under ``static/uploads`` for local development.
if os.environ.get("VERCEL"):
    UPLOAD_FOLDER = os.path.join("/tmp", "uploads")
else:
    UPLOAD_FOLDER = os.path.join("static", "uploads")

os.makedirs(UPLOAD_FOLDER, exist_ok=True)


def allowed_file(filename):
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/upload", methods=["GET", "POST"])
def upload_file():
    if request.method == "POST":
        if "file" not in request.files:
            return "Dosya bulunamadı", 400
        file = request.files["file"]
        if file.filename == "":
            return "Dosya seçilmedi", 400
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            ext = os.path.splitext(filename)[1].lower()
            unique_name = f"{uuid.uuid4().hex}{ext}"
            file.save(os.path.join(UPLOAD_FOLDER, unique_name))
            return render_template("success.html")
        else:
            return "Geçersiz dosya türü", 400
    return render_template("upload.html")


@app.route("/image/<filename>")
def view_image(filename):
    file_path = os.path.join(UPLOAD_FOLDER, filename)
    if not os.path.exists(file_path):
        abort(404)
    return send_file(file_path)


@app.route("/download/<filename>")
def download_image(filename):
    file_path = os.path.join(UPLOAD_FOLDER, filename)
    if not os.path.exists(file_path):
        abort(404)
    return send_file(
        file_path,
        as_attachment=True,
        download_name=filename,
    )


@app.route("/gallery")
def gallery():
    images = [f for f in os.listdir(UPLOAD_FOLDER) if allowed_file(f)]
    images.sort(reverse=True)
    return render_template("gallery.html", images=images)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)

