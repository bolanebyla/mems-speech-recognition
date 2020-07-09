import flask
import json

from flask import request
from flask import render_template
from bot import *

from prediction import get_prediction_text

app = flask.Flask(__name__, template_folder='templates', static_folder='static')


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
        prediction_text, class_name = get_prediction_text(wavfiles)  # Предсказание модели
        print(prediction_text, class_name)
        data = json.dumps({'data': prediction_text})  # Записываем в json
        return data


@app.route('/bot/' + TOKEN, methods=['GET', 'POST'])
def webhook():
    bot.process_new_updates([telebot.types.Update.de_json(request.stream.read().decode("utf-8"))])
    return 'ok', 200


if __name__ == '__main__':
    app.run()
