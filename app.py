import os
import subprocess
import flask
import pickle
import ffmpeg

import numpy as np
from flask import request
from flask import jsonify
from flask import render_template
from werkzeug.utils import secure_filename

from model import get_model, get_prediction
from sound import get_audio

app = flask.Flask(__name__, template_folder='templates', static_folder='static')

CLASSES = ['ГРУСТЬ', 'МЕМ']  # Классы команд (без фона)

model = get_model()
model.load_weights("model-cnn.h5")

uploads_dir = os.path.join(app.instance_path, 'uploads')


@app.route('/', methods=['GET', 'POST'])
def index():
    if flask.request.method == 'GET':
        return render_template('index.html')

    if flask.request.method == 'POST':
        voice = request.files.get('voice')
        print(voice)
        voice.save('uploads/recording.wav')
        print('uploaded')

        #subprocess.call(['ffmpeg', '-i', 'uploads/recording.wav',
         #                'uploads/recording1.wav'])

        #get_audio(voice.read())

        wavfiles = 'uploads/1.wav'  # Получаем имя очередного файла
        print(get_prediction(wavfiles, model, CLASSES))

    return render_template('index.html', result=get_prediction(wavfiles, model, CLASSES))


if __name__ == '__main__':
    app.run()
