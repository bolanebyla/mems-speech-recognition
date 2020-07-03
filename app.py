import flask
import pickle

import numpy as np

from model import get_model, get_prediction

app = flask.Flask(__name__, template_folder='templates')

CLASSES = ['ГРУСТЬ', 'МЕМ']  # Классы команд (без фона)

model = get_model()
model.load_weights("model-cnn.h5")


@app.route('/', methods=['GET', 'POST'])
def index():
    # if flask.request.method == 'GET':
    # if flask.request.method == 'POST':
    wavfiles = 'одинокий мем 4.wav'  # Получаем имя очередного файла
    print(get_prediction(wavfiles, model, CLASSES))
    return f'<h1>{get_prediction(wavfiles, model, CLASSES)}</h1>'


if __name__ == '__main__':
    app.run()
