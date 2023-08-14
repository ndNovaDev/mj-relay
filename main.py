from flask import Flask, jsonify, make_response, send_file
import os
import requests
import io
from PIL import Image
from rembg import remove

def serve_pil_image(pil_img):
    img_io = io.BytesIO()
    pil_img.save(img_io, 'png', quality=70)
    img_io.seek(0)
    return send_file(img_io, mimetype='image/png')

app = Flask(__name__)


@app.route('/')
def index():
    return jsonify({"Choo Choo": "Welcome to your Flask app 🚅"})

@app.route('/imagine')
def imagine():
    image_url = 'https://cdn.discordapp.com/attachments/1140481534760067198/1140559999102353518/novadev__Phone_settings_button_Windows_Vista_style_solid_color__cb030d47-10ab-4185-8b33-e2d55a5f8640.png'
    image_response = requests.get(image_url)
    pil_ori = Image.open(io.BytesIO(image_response.content))
    (width, height) = pil_ori.size
    pil_cropped = pil_ori.crop((0, 0, width / 2, height / 2))
    bg_removed = remove(pil_cropped)
    return serve_pil_image(bg_removed)

if __name__ == '__main__':
    app.run(debug=True, port=os.getenv("PORT", default=8000))
