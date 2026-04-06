import os
from flask import Flask, request, render_template_string, send_from_directory

app = Flask(__name__)
# 保存先フォルダの設定
UPLOAD_FOLDER = 'uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# スマホで見やすいデザイン（HTML/CSS）
HTML_TEMPLATE = """
<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>スマホ共有</title>
    <style>
        body { font-family: sans-serif; padding: 20px; text-align: center; background: #f0f4f8; }
        .card { background: white; padding: 20px; border-radius: 15px; box-shadow: 0 4px 6px rgba(0,0,0,0.1); }
        input[type="file"] { margin: 20px 0; }
        button { background: #007bff; color: white; border: none; padding: 10px 20px; border-radius: 5px; font-size: 16px; }
        ul { list-style: none; padding: 0; text-align: left; }
        li { background: #fff; margin: 5px 0; padding: 10px; border-radius: 5px; border-bottom: 1px solid #eee; }
        a { text-decoration: none; color: #007bff; word-break: break-all; }
    </style>
</head>
<body>
    <div class="card">
        <h2>📁 ファイル共有</h2>
        <form method="post" enctype="multipart/form-data" action="/upload">
            <input type="file" name="file"><br>
            <button type="submit">アップロード開始</button>
        </form>
        <hr>
        <h3>↓ 送信済みファイル</h3>
        <ul>
            {% for file in files %}
            <li><a href="/download/{{ file }}" download>{{ file }}</a></li>
            {% endfor %}
        </ul>
    </div>
</body>
</html>
"""

@app.route('/')
def index():
    files = os.listdir(UPLOAD_FOLDER)
    return render_template_string(HTML_TEMPLATE, files=files)

@app.route('/upload', methods=['POST'])
def upload_file():
    file = request.files.get('file')
    if file and file.filename:
        file.save(os.path.join(UPLOAD_FOLDER, file.filename))
    return '<script>alert("完了！"); window.location.href="/";</script>'

@app.route('/download/<filename>')
def download_file(filename):
    return send_from_directory(UPLOAD_FOLDER, filename)

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
