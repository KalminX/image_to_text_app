import os
from flask import Flask, render_template, request, redirect, url_for
from werkzeug.utils import secure_filename
from PIL import Image
import pytesseract
import logging
from datetime import datetime

app = Flask(__name__)
UPLOAD_FOLDER = 'static/uploads'
LOG_FILE = 'logs/access.log'

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(os.path.dirname(LOG_FILE), exist_ok=True)

# Logging configuration
logging.basicConfig(filename=LOG_FILE, level=logging.INFO,
                    format='%(asctime)s - %(message)s')

def log_usage(ip):
    logging.info(f"Accessed by IP: {ip}")

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        log_usage(request.remote_addr)
        if 'image' not in request.files:
            return redirect(request.url)

        file = request.files['image']
        if file.filename == '':
            return redirect(request.url)

        filename = secure_filename(file.filename)
        path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(path)

        try:            
            image = Image.open(path)
            image.save(path)

            # Convert to grayscale first (optional)
            gray_image = image.convert("L")

            # Convert to pure black and white (binary)
            bw_image = gray_image.point(lambda x: 0 if x < 128 else 255, '1')

            # Now run OCR on the cleaned image
            text = pytesseract.image_to_string(bw_image)
            # text = pytesseract.image_to_string(img)
        except Exception as e:
            text = f"Error reading image: {e}"

        return render_template('result.html', text=text)

    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True, port=8000)
