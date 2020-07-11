import os
import random
import telebot
import requests
import subprocess
from prediction import get_prediction_text

TOKEN = os.environ.get('TG_TOKEN')
HOST = os.environ.get('HOST')
print(TOKEN)
print(HOST)
bot = telebot.TeleBot(TOKEN, threaded=False)
bot.set_webhook(url=HOST + 'bot/' + TOKEN)


# Команда /start
@bot.message_handler(commands=['start'])
def start_message(message):
    chat_id = message.chat.id
    bot.send_message(chat_id=chat_id, text='Привет!')
    bot.send_message(chat_id=chat_id, text='Доступные голосовые команды:\n'
                                           '- МЕМ\n'
                                           '- ГРУСТЬ')


@bot.message_handler(content_types=['voice'])
def voice_processing(message):
    chat_id = message.chat.id

    file_info = bot.get_file(message.voice.file_id)
    audio = requests.get('https://api.telegram.org/file/bot{0}/{1}'.format(TOKEN, file_info.file_path)).content

    with open("uploads/bot/audio_file.Ogg", "wb") as file:
        file.write(audio)
    subprocess.call(
        ['ffmpeg',
         '-i',
         'uploads/bot/audio_file.Ogg',
         '-y',
         'uploads/bot/audio_file.wav',
         '-hide_banner'])  # Перезаписываем с нужной кодировкой

    wavfiles = 'uploads/bot/audio_file.wav'  # Имя очередного файла
    prediction_text, class_name = get_prediction_text(wavfiles)  # Предсказание модели
    print(prediction_text, class_name)

    bot.send_message(chat_id=chat_id, text=prediction_text)

    # Отправляем изображение, если команда распознана
    if class_name:
        if class_name == 'МЕМ':
            directory = 'static/img/memes/'
            photo = open(os.path.join(directory , random.choice(os.listdir(directory))), 'rb')
        else:
            directory = 'static/img/sadness/'
            photo = open(os.path.join(directory, random.choice(os.listdir(directory))), 'rb')
        bot.send_photo(chat_id=chat_id, photo=photo)


if __name__ == '__main__':
    bot.skip_pending = True
    bot.remove_webhook()
    print('bot запущен...')
    bot.polling()
