import os
import subprocess
import flask
import json
import pickle

from flask import request
from flask import render_template

from model import get_model, get_prediction

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
        voice.save('uploads/recording.wav')  # Сохраняем аудио
        subprocess.call(
            ['ffmpeg',
             '-i',
             'uploads/recording.wav',
             '-y',
             '-hide_banner'])  # Перезаписываем с нужной кодировкой

        wavfiles = 'uploads/recording.wav'  # Имя очередного файла
        prediction = get_prediction(wavfiles, model, CLASSES)  # Предсказание модели
        print(prediction)
        data = json.dumps({'data': prediction})  # Записываем в json
        return data


if __name__ == '__main__':
    app.run()
