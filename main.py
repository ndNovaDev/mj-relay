from flask import Flask, jsonify
import requests
from PIL import Image
from io import BytesIO
from base64 import b64encode
from os import getenv

app = Flask(__name__)

@app.route('/')
def index():
    return jsonify({"Choo Choo": "Welcome to your Flask app 🚅"})
    
@app.route('/mj/task/<id>')
def get_task_status(id):
    mj_status_url = getenv('mj.relay.domain', default='https://midjourney-proxy-production-77c1.up.railway.app') + '/mj/task/{id}/fetch'.format(id=id)
    mj_status_response = requests.get(mj_status_url).json()
    progress_str = mj_status_response['progress']
    response = {
        "status": mj_status_response['status'],
        "progress": 0 if progress_str == '' else int(progress_str[:-1]),
        "image": Null if mj_status_response['status'] != 'SUCCESS' else get_mj_image(mj_status_response['imageUrl']) 
    }
    return jsonify(response)

def get_mj_image(mj_image_url):
    image_response = requests.get(mj_image_url)

    pil_ori = Image.open(BytesIO(image_response.content))
    (width, height) = pil_ori.size
    pil_cropped = pil_ori.crop((0, 0, width / 2, height / 2))

    return pil_image_to_base64(pil_cropped)

def pil_image_to_base64(image):
    buffered = BytesIO()
    image.save(buffered, format="JPEG")
    return 'data:image/jpeg;base64,' + b64encode(buffered.getvalue()).decode('utf-8')

if __name__ == '__main__':
    app.run(debug=True, port=getenv("PORT", default=3000))

