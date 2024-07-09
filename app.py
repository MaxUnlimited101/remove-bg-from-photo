from flask import Flask, request, jsonify, send_file
import os
from rembg import remove
from PIL import Image
import zipfile
import shutil

app = Flask(__name__)

file = open('./public/index.html')
html = file.read()
file.close()

@app.route("/")
def hello_world():
    return html

@app.route('/upload', methods=['POST'])
def upload_files():
    if 'files[]' not in request.files:
        return jsonify({'message': 'No files part in the request'}), 400

    files = request.files.getlist('files[]')
    
    if len(files) == 0:
        return jsonify({'message': 'No files selected for uploading'}), 400

    folder = './uploads/'
    if not os.path.isdir(folder):
        os.mkdir(folder)
    else:
        for filename in os.listdir(folder):
            file_path = os.path.join(folder, filename)
            try:
                if os.path.isfile(file_path) or os.path.islink(file_path):
                    os.unlink(file_path)
                elif os.path.isdir(file_path):
                    shutil.rmtree(file_path)
            except Exception as e:
                print('Failed to delete %s. Reason: %s' % (file_path, e))

    zipf = zipfile.ZipFile('./uploads/images.zip','w', zipfile.ZIP_DEFLATED)

    for file in files:
        if file.filename == '':
            return jsonify({'message': 'One or more files have an empty filename'}), 400
        name = "(removed bg)" + os.path.splitext(file.filename)[0] + '.png'
        out_name = os.path.join('uploads', name)
        remove_bg(file, out_name)
        zipf.write(out_name, os.path.basename(out_name))
        os.remove(out_name)

    zipf.close()
    return jsonify({'message': 'OK'}), 200

def remove_bg(file, name: str) -> Image:
    inp = Image.open(file)
    out = remove(inp)
    out.save(name)
    
@app.route('/uploads/images.zip', methods=['GET'])
def download_result():
    return send_file('./uploads/images.zip', as_attachment=True, download_name='remove-background.zip')