import os
import subprocess
import time
from flask import Flask, render_template, request, send_file, redirect, url_for
from werkzeug.utils import secure_filename

app = Flask(__name__, template_folder='templates',
            static_folder='static')
app.config['UPLOAD_FOLDER'] = os.path.join(
    os.getcwd(), "static", "uploads")
app.config['UPSCALED_FOLDER'] = os.path.join(os.getcwd(), "static", "upscaled")


@app.route("/")
@app.route("/home")
def home():
    return render_template('index.html')


@app.route("/download", methods=["POST"])
def download():
    file = request.files['uploadedFile']

    if file:
        filename = secure_filename(file.filename)

        input_path = os.path.join(
            app.config['UPLOAD_FOLDER'], str(time.time()) + '_' + filename)

        file.save(input_path)

        output_path = os.path.join(app.config['UPSCALED_FOLDER'], str(
            time.time()) + '_upscaled_' + filename)

        enhance_image(input_path, output_path)

        after_preview_path = url_for(
            'static', filename='upscaled/' + os.path.basename(output_path))

        return render_template('preview.html', download_img=output_path, output_image=after_preview_path)
    else:
        return redirect(url_for("home"))


@app.route("/download/<filename>")
def download_image(filename):
    download_file = send_file(filename, as_attachment=True)
    return download_file


def enhance_image(input, output):
    realesrgan_path = os.path.join(
        os.getcwd(), "RealESRGAN", "realesrgan-ncnn-vulkan.exe")
    command_statement = [realesrgan_path, '-i', input, '-o', output]
    subprocess.Popen(command_statement,
                     creationflags=subprocess.CREATE_NO_WINDOW).wait()


if __name__ == "__main__":
    app.run(debug=True)
