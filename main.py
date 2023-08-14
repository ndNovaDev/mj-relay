from flask import Flask, jsonify, make_response, send_file
import os
import requests
import io
from PIL import Image

def serve_pil_image(pil_img):
    img_io = io.BytesIO()
    pil_img.save(img_io, 'JPEG', quality=70)
    img_io.seek(0)
    return send_file(img_io, mimetype='image/jpeg')

app = Flask(__name__)


@app.route('/')
def index():
    return jsonify({"Choo Choo": "Welcome to your Flask app 🚅"})

@app.route('/imagine')
def imagine():
    image_url = 'https://cdn.discordapp.com/attachments/1140481534760067198/1140537223905812500/novadev__Cat_2b38604a-4df1-47dc-b98b-07f3692f1f57.png'
    image_response = requests.get(image_url)
    pil_ori = Image.open(io.BytesIO(image_response.content))
    (width, height) = pil_ori.size
    pil_cropped = pil_ori.crop((0, 0, width / 2, height / 2))
    return serve_pil_image(pil_cropped)

if __name__ == '__main__':
    app.run(debug=True, port=os.getenv("PORT", default=5000))
