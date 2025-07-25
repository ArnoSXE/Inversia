from flask import Flask, render_template, request, redirect, send_from_directory
import os
from werkzeug.utils import secure_filename

UPLOAD_FOLDER = 'uploads'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

RENDER_URL = "https://inversia-ba86.onrender.com"  # ✅ Your Render app's public URL

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route("/", methods=["GET", "POST"])
def index():
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

            engines = request.form.getlist('engine')
            urls = []
            for engine in engines:
                url = ""
                if engine == "google":
                    url = f"https://lens.google.com/uploadbyurl?url={RENDER_URL}/uploads/{filename}"  # ✅ fixed here
                elif engine == "yandex":
                    url = f"https://yandex.com/images/search?rpt=imageview&url={RENDER_URL}/uploads/{filename}"  # ✅ fixed here
                elif engine == "bing":
                    url = f"https://www.bing.com/images/search?q=imgurl:{RENDER_URL}/uploads/{filename}&view=detailv2"  # ✅ fixed here
                if url:
                    urls.append(url)

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

