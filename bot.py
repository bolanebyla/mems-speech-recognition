import telebot
import requests
import subprocess
from model import get_prediction

TOKEN = '1378189568:AAFcZV-g3lmahSZlcB1_9PnerNrTiVNvo_4'
HOST = '341088-cs07173.tmweb.ru/'
bot = telebot.TeleBot(TOKEN, threaded=False)
bot.set_webhook(url=HOST + 'bot/' + TOKEN)


# Команда /start
@bot.message_handler(commands=['start'])
def start_message(message):
    chat_id = message.chat.id
    bot.send_message(chat_id=chat_id, text='Привет!\n')


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
    prediction = get_prediction(wavfiles)  # Предсказание модели
    print(prediction)
    bot.send_message(chat_id=chat_id, text=prediction)


if __name__ == '__main__':
    bot.skip_pending = True
    bot.remove_webhook()
    print('bot запущен...')
    bot.polling()
