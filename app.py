from flask import Flask, render_template, request, redirect, url_for
from werkzeug.utils import secure_filename
import firebase_admin
from firebase_admin import credentials, storage

app = Flask(__name__, template_folder='templates', static_folder='static')

app.config['FIREBASE_ADMIN'] = {
    "type": "service_account",
    "project_id": "practice-e99ea",
    "private_key_id": "18ebc29508be1e5253e28adb09ade76ee1407d8a",
    "private_key": "-----BEGIN PRIVATE KEY-----\nMIIEvQIBADANBgkqhkiG9w0BAQEFAASCBKcwggSjAgEAAoIBAQC6POT7xGE53uLK\nSYsok4TwmMCXBq6GEa95enN0j97eXXcBEqWRBnU87DXKUz1Vtkf6hiwQaNHbCvDd\ne2pcG77DS+TiNwNyI1EcfZeXmBdeRAoZFbBaLGaJssJY1FSStBeiwHIKUYr/GTdh\ncsNqTh4sXO2HP4xTx7uPLdDbI1+xgRFcaztNTVDWwpjpssYuOIBSuw3Ood3QltFG\n3K/EI1q3xCORW8oN2TWyt0pbkNjTWtJPCNkyd4WnIBzSAXDC0/7sJp7c9GoNFmc5\nK4/cF1jS57vuxOWe9AJJZ7WTucqrk0qmzt34YSGx0Nul9XSUls4GPC2vjv3a7KKV\nCfmGd6JxAgMBAAECggEAEZjsaA+zwiSZ2FRfpkteHd/JHtweRIPKSVe1LhfkDq3V\nL1BEPbJXBJUrNf1sh7tMDNN9uWU2IxTjEoJ1V9O1UD3NGETree71XJRPbR8NYjZa\nn+kpOzQD0lIGRB94CE6lBxdZDzmKQTVwQrB134cXGckEFqn+B/KQ+ePx3qr2gU6P\n2aeWLOtWt6SR54uBHbC5jc4I7YDzfrToTAfU472u3FiDBeOIYGjhtR3DjuKaPff+\ncH1tmCXnnI4X2iLnokFo2KpJ57Ocl0PEXVXKqOu9aW5hFvLtuhP+1JacgooaSXuc\nYTFZL4PlHVgB99jb7xXFYTGpLOUzx4+GvDiBlxoEMwKBgQDuX4srcE4wLMaeFAHU\nwKNdz7toiuIP6I2+Vu4gtLfRycVh6bh/51R8rYVXRqm5DPc424YY2B/sAG6yoxHW\naZKsXVgbs2Iq8tXuommppt7iX1oPdtdxBgnC+Hd7z4qi9qRxHOVjdUSNChjM8Pmj\nVLK1LMpAu9I9mauTpOLRiPFuXwKBgQDIAmregK7cFMZxL/YpKt2oBOLiPXMozqgR\nmKLuE/bo29TSdrrdA6208sd4ZecOjcODRdXM9WOel81SxnVT5enyC7X+oC0Nzy8F\nJEzdb1llrkk2l/cvEAcrLhH52RO7o71Zs61QD6+kv1G6LAfAzGX4G/sJRJVYr76D\nlx3XfwoBLwKBgGEU0nY/h+iA4+dPmKtQRXiYeOgL4CPAf7Hsb5EsaMztExFcgcK9\nsSAR/4NbCRaPnEQwy71kkCOqzWq9lS8w0gaXAaJOfYWmXtCQnt30U0P4t5IiwX2L\niwA391maXgke0DwtG5NVGDUkzpLw9Yq6nQnCkyCoHejuo/0+ow3ZaxKbAoGARAtO\ngFQXKRiISomenXLP5hGDfqSZQRDNbO8YvxZbsezYAqISAI730c+mvPcuHG1uToK7\nsfbp5VKPr9GEqP5XENmbGP01VrVdscofvFXdfBJHJiOdHI2/YplR1EZdyEB0csgF\n9m7fupS8ITJJkPX42ufqB8Ulaf6gOfR3WpEFvlECgYEA47rQUIreywN+fFW+25PP\njUcMAHZXkxDowR0ysA+J1jiSdJcKXmO1tFTvfphjwL8CA4iJ8M6pKZuzKgWPIDPl\nD06zuhBXuw1NsFDhDwWF4XYzWLMjIqtRm7J/0PXqIvPBNZKpSA94+BlBJrp0bpJQ\ndAxre6WiVWIXafqoy0zvILw=\n-----END PRIVATE KEY-----\n",
    "client_email": "firebase-adminsdk-jk3k9@practice-e99ea.iam.gserviceaccount.com",
    "client_id": "104260545072075852000",
    "auth_uri": "https://accounts.google.com/o/oauth2/auth",
    "token_uri": "https://oauth2.googleapis.com/token",
    "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
    "client_x509_cert_url": "https://www.googleapis.com/robot/v1/metadata/x509/firebase-adminsdk-jk3k9%40practice-e99ea.iam.gserviceaccount.com"
}

firebase_cred = credentials.Certificate(app.config['FIREBASE_ADMIN'])
firebase_admin.initialize_app(firebase_cred, {'storageBucket': 'practice-e99ea.appspot.com'})

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
    download_url = blob.generate_signed_url(version="v4", method="GET", expiration=3600)
    return redirect(download_url)


if __name__ == "__main__":
    app.run(debug=True)
