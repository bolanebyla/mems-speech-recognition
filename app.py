import os
import flask
import json
import pickle

from flask import request
from flask import render_template
from bot import *

#from model import get_model, get_prediction

app = flask.Flask(__name__, template_folder='templates', static_folder='static')

CLASSES = ['ГРУСТЬ', 'МЕМ']  # Классы команд (без фона)

#model = get_model()
#model.load_weights("model-cnn.h5")

uploads_dir = os.path.join(app.instance_path, 'uploads')


@app.route('/', methods=['GET', 'POST'])
def index():
    if flask.request.method == 'GET':
        return render_template('index.html')

    if flask.request.method == 'POST':
        voice = request.files.get('voice')
        voice.save('uploads/web/recording.wav')  # Сохраняем аудио
        subprocess.call(
            ['ffmpeg',
             '-i',
             'uploads/web/recording.wav',
             '-y',
             '-hide_banner'])  # Перезаписываем с нужной кодировкой

        wavfiles = 'uploads/web/recording.wav'  # Имя очередного файла
        #prediction = get_prediction(wavfiles, model, CLASSES)  # Предсказание модели
        prediction = 'тестовый предикт web'
        print(prediction)
        data = json.dumps({'data': prediction})  # Записываем в json
        return data

@app.route('/bot/' + TOKEN, methods=['GET', 'POST'])
def webhook():
    print('пришло', request)
    bot.process_new_updates([telebot.types.Update.de_json(request.stream.read().decode("utf-8"))])
    return 'ok', 200

if __name__ == '__main__':
    app.run()
