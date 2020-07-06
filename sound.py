import librosa
import numpy as np

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



