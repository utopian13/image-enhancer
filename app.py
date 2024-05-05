from flask import Flask, render_template, request, send_file, redirect, url_for
from werkzeug.utils import secure_filename
import firebase_admin
from firebase_admin import credentials, storage

app = Flask(__name__, template_folder='templates', static_folder='static')
cred = credentials.Certificate("firebase-sdk.json")
firebase_admin.initialize_app(
    cred, {'storageBucket': 'practice-e99ea.appspot.com'})

bucket = storage.bucket()


@app.route("/")
@app.route("/home")
def home():
    return render_template('index.html')


@app.route("/upload", methods=["POST"])
def upload():
    file = request.files['uploadedFile']
    if file:
        filename = secure_filename(file.filename)
        blob = bucket.blob(filename)
        blob.upload_from_file(file)
        output_image_url = blob.public_url

        return render_template('preview.html', download_img=filename, output_image=output_image_url)
    else:
        return redirect(url_for("home"))


@app.route("/download/<filename>")
def download(filename):
    blob = bucket.blob(filename)
    download_url = blob.generate_signed_url(
        version="v4", method="GET", expiration=3600)
    return redirect(download_url)


if __name__ == "__main__":
    app.run(debug=True)
