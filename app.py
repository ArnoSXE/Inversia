from flask import Flask, render_template, request, redirect, send_from_directory
import os
from werkzeug.utils import secure_filename

UPLOAD_FOLDER = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'uploads')
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Ensure the upload folder exists
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

RENDER_URL = "https://inversia-ba86.onrender.com"  

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route("/", methods=["GET", "POST"])
def index():
    public_url = f"https://{request.host}"
    
    if request.method == "POST":
        if 'image' not in request.files:
            return "No file part"
        file = request.files['image']
        if file.filename == '':
            return "No selected file"
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(filepath)

            # Schedule file deletion after 1 minute (60 seconds)
            import threading
            import time
            def delete_file(path):
                time.sleep(60)
                if os.path.exists(path):
                    os.remove(path)
            threading.Thread(target=delete_file, args=(filepath,)).start()

            engines = request.form.getlist('engine')
            urls = []
            image_url = f"{public_url}/uploads/{filename}"
            # URL encode the image URL for search engines
            import urllib.parse
            encoded_image_url = urllib.parse.quote(image_url, safe='')
            
            for engine in engines:
                if engine == "google":
                    urls.append(f"https://lens.google.com/uploadbyurl?url={encoded_image_url}")
                elif engine == "yandex":
                    urls.append(f"https://yandex.com/images/search?url={encoded_image_url}&rpt=imageview")
                elif engine == "bing":
                    urls.append(f"https://www.bing.com/images/search?q=imgurl:{encoded_image_url}&view=detailv2&iss=sbi")

            return render_template("index.html", urls=urls)

    return render_template("index.html", urls=None)

@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

if __name__ == "__main__":
    if not os.path.exists(UPLOAD_FOLDER):
        os.makedirs(UPLOAD_FOLDER)
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=False)

