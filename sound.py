import librosa
import numpy as np
import ffmpeg
from base64 import b64decode
import io
from scipy.io.wavfile import read as wav_read


def wav2mfcc(file_path, length=11025, step=2205):
    out_mfcc = []  # Выходной массив, содержащий mfcc исходного файла с шагом step
    out_audio = []  # Выходной массив, содеражищий аудиоинформацию исходного файла с шагом step
    y, sr = librosa.load(file_path, duration=5.0)  # Загружаем данные исходного файла

    while (len(
            y) >= length):  # Проходим весь массив y, пока оставшийся кусочек не станет меньше указанной в параметре max_len длинны
        section = y[:length]  # Берем начальный кусок длинной length
        section = np.array(section)  # Переводим в numpy
        out_mfcc.append(
            librosa.feature.mfcc(section, sr))  # Добавляем в выходной массив out_mfcc значение mfcc текущего куска
        out_audio.append(section)  # Добавляем в выходной массив аудио текущий кусок
        y = y[step:]  # Уменьшаем y на step

    out_mfcc = np.array(out_mfcc)  # Преобразуем в numpy
    out_audio = np.array(out_audio)  # Преобразуем в numpy
    return out_mfcc, out_audio  # функция вернет массив мэл-частот и массив аудио-отре


def get_audio(data):  # объявляем функцию извлечения аудио, записанного через микрофон в ноутбуке
    print(data)
    # data сейчас в таком виде: 'data:audio/webm;codecs=opus;base64,GkXfo59ChoEBQveBAULygQRC84EIQoKEd2VibUKHgQRChYE...mpZpkq1'
    binary = b64decode(
        data)  # отсекаем информацию "data:audio/webm;codecs=opus;base64", оставляем только данные и декодируем
    # b'\x1aE\xdf\xa3\x9fB\x86\x81\x01B\xf7\x81\x01B\xf2

    process = (ffmpeg
               .input('pipe:0')  # поток стандартного ввода
               .output('pipe:1', format='wav')  # стандартного вывода в формате wav
               .run_async(pipe_stdin=True, pipe_stdout=True, pipe_stderr=True, quiet=True,
                          overwrite_output=True))  # асинхронное выполнение командной строки FFmpeg
    print('nen')
    # binary преобразовываем в wav, с типичным для медиафайлов форматом RIFF(ResourceInterchangeFileFormat - формат файла для обмена ресурсами)
    output, err = process.communicate(input=binary)
    # output - b'RIFF\xff\xff\xff\xffWAVEfmt \x10\x00\x00\x00\x01\x00\x01\x00\x80\xbb\x00\x00\...\x01\x00\x01\x00\x01\x0\xff'
    # err - b"ffmpeg version 3.4.6-0ubuntu0.18.04.1 Copyright (c) 2000-2019 the FFmpeg developers\n...headers:0kB muxing overhead: 0.046695%\n"

    # Cодержимое файла группируется из отдельных секций (chunks) - формат выборок аудиоданных. Секция имеет свой заголовок и данные секции.
    # Размер заголовка секции RIFF - 8 байт, их ниже уберём из определения размера секции RIFF
    riff_chunk_size = len(output) - 8
    # Разбиваем размер секции на четыре байта, которые запишем далее в b.
    q = riff_chunk_size
    b = []
    for i in range(4):
        q, r = divmod(q, 256)  # возьмем размер секции и вернем частное и остаток от деления на 256, и так 4 раза
        b.append(r)  # каждый из остатков добавим в список

    # Меняем байты c 4го по 7й вкл-но('\xff\xff\xff\xff') в output на b (типа '\xc62\x02\x00')
    riff = output[:4] + bytes(b) + output[8:]

    # класс io.BytesIO позволит работать с последовательностью байтов как с файловым объектом, а далее прочитаем как wav файл
    sr, audio = wav_read(io.BytesIO(riff))  # извлечём частоту дискретизации и полученный сигнал

    return audio, sr  # функция вернет полученный сигнал и частоту дискретизации
