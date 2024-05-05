from flask import Flask, render_template, request, send_file, redirect, url_for
from werkzeug.utils import secure_filename
import firebase_admin
from firebase_admin import credentials, storage
from dotenv import load_dotenv
import os

load_dotenv()

app = Flask(__name__, template_folder='templates', static_folder='static')

firebase_admin_key = {
    "type": "service_account",
    "project_id": "your-project-id",
    "private_key_id": os.getenv("FIREBASE_ADMIN_PRIVATE_KEY_ID"),
    "private_key": os.getenv("FIREBASE_ADMIN_PRIVATE_KEY").replace("\\n", "\n"),
    "client_email": os.getenv("FIREBASE_ADMIN_CLIENT_EMAIL"),
    "client_id": os.getenv("FIREBASE_ADMIN_CLIENT_ID"),
    "auth_uri": "https://accounts.google.com/o/oauth2/auth",
    "token_uri": "https://oauth2.googleapis.com/token",
    "auth_provider_x509_cert_url": os.getenv("FIREBASE_ADMIN_AUTH_PROVIDER_X509_CERT_URL"),
    "client_x509_cert_url": os.getenv("FIREBASE_ADMIN_CLIENT_X509_CERT_URL")
}

firebase_cred = credentials.Certificate(firebase_admin_key)
firebase_admin.initialize_app(firebase_cred)

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
