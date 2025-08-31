from flask import (
    Flask,
    request,
    render_template,
    send_file,
    abort,
)
from werkzeug.utils import secure_filename
from io import BytesIO
import os
import sqlite3

ALLOWED_EXTENSIONS = {"png", "jpg", "jpeg", "gif"}

app = Flask(__name__)

DATABASE = os.path.join(os.path.dirname(__file__), "images.db")


def init_db():
    conn = sqlite3.connect(DATABASE)
    conn.execute(
        """
        CREATE TABLE IF NOT EXISTS images (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            filename TEXT NOT NULL,
            mimetype TEXT NOT NULL,
            data BLOB NOT NULL
        )
        """
    )
    conn.commit()
    conn.close()


init_db()


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
            data = file.read()
            mimetype = file.content_type
            conn = sqlite3.connect(DATABASE)
            conn.execute(
                "INSERT INTO images (filename, mimetype, data) VALUES (?, ?, ?)",
                (filename, mimetype, data),
            )
            conn.commit()
            conn.close()
            return render_template("success.html")
        else:
            return "Geçersiz dosya türü", 400
    return render_template("upload.html")


@app.route("/image/<int:image_id>")
def view_image(image_id):
    conn = sqlite3.connect(DATABASE)
    cur = conn.execute(
        "SELECT data, mimetype FROM images WHERE id = ?", (image_id,)
    )
    row = cur.fetchone()
    conn.close()
    if row:
        data, mimetype = row
        return send_file(BytesIO(data), mimetype=mimetype)
    abort(404)


@app.route("/download/<int:image_id>")
def download_image(image_id):
    conn = sqlite3.connect(DATABASE)
    cur = conn.execute(
        "SELECT filename, data, mimetype FROM images WHERE id = ?", (image_id,)
    )
    row = cur.fetchone()
    conn.close()
    if row:
        filename, data, mimetype = row
        return send_file(
            BytesIO(data),
            mimetype=mimetype,
            as_attachment=True,
            download_name=filename,
        )
    abort(404)


@app.route("/gallery")
def gallery():
    conn = sqlite3.connect(DATABASE)
    cur = conn.execute("SELECT id, filename FROM images ORDER BY id DESC")
    images = [dict(id=row[0], filename=row[1]) for row in cur.fetchall()]
    conn.close()
    return render_template("gallery.html", images=images)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)

