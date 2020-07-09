import numpy as np
from keras.models import model_from_json
from sound import wav2mfcc

sample_rate = 22050  # Значение sample_rate аудиофайлов
feature_dim_1 = 20  # стандартная величина MFCC признаков
feature_dim_2 = int(.5 * sample_rate)  # установленная длина фреймов (в секундах 0.5 = 500 мс)
step_mfcc = int(.1 * sample_rate)  # Шаг смещения при разборе mfcc (в секундах 0.1 = 100мс)
channel = 1  # количество каналов
n_classes = 3  # Количество классов команд

CLASSES = ['ГРУСТЬ', 'МЕМ']  # Классы команд (без фона)

# Загружаем модель
with open('model-mem.json', 'r') as f:
    model = model_from_json(f.read())

# Загружаем веса модели
model.load_weights("model-cnn.h5")


# Предсказание команды
def predict(namefile, model, min_count=2, rate=0.9,
            hole=1):  # функция принимает на вход путь к нужному файлу, и имя обученной модели
    mfcc_full, audio_full = wav2mfcc(namefile, length=feature_dim_2,
                                     step=step_mfcc)  # Получаем массив mfcc выбранного файла с именем namefile

    # mfcc = xScaler.transform(mfcc_full.reshape(-1,1))
    mfcc_full = mfcc_full.reshape(-1, 20, 22, 1)
    g_pred = model.predict(mfcc_full)  # Предиктим с помощью модели model массив mfcc
    pred = np.array([np.argmax(i) for i in
                     g_pred])  # Выбираем индекс максимального элемента в каждом g_pred[i]  и создаем numpy-массив pred из этих индексов
    out = []  # Объявляем выходную переменную out (В ней будут храниться преобразованные из mfcc ауидоданные, класс команды и точность, с которой сеть считает эту команду верной)

    # Ищем команды каждого класса
    for idx_class in range(n_classes - 1):
        idxs = np.where(
            pred == idx_class)  # В массиве pred находим все элементы со значением, равным искомому классу idx_class
        idxs = idxs[0]  # Размерность полученного маасива в np.where иммет тип (x,). Оставляем только первую размерность
        if (len(idxs) == 0):  # Если элементы искомого класса не найдены,
            continue  # то переходим к поиску команд следующего класса

        curr = []  # Временный массив для хранения информации о найденных командах
        '''
        в массиве idx данные прдеставлены следующим образом:
        [4, 5, 6, 7, 123, 124, 125, 126, 127]
        в массив curr мы запишем [4, 123] только стартовые индексы
        поскольку очевидно, что 4,5,6,7 и 123,124,125,126,127 представляют единую команду
        '''
        curr_idx = int(idxs[0])  # Текущий стартовый индекс
        summ, length = 0, 0  # summ - хранит сумму вероятностей, с которой сеть отнесла команду к данному классу; length - длинна последовательно идущих элементов для одной команды (для массива curr из примера
        # [4, 123] длина соответствующая первому элементу будет 4, второму - 5 )
        for i in range(len(idxs)):  # Пробегаем по всему массиву idxs
            summ += g_pred[idxs[i]][idx_class]  # Считаем сумму вероятности
            length += 1  # Увеличиваем длинну последовательности
            if i == len(idxs) - 1:  # Если последний элемент последовательности
                if (
                        length >= min_count and summ / length >= rate):  # Проверяем на условия разбора: длинна последовательности должна быть больше входного параметра min_count
                    # summ / length должно быть больше входного параметра rate
                    curr.append([curr_idx, length,
                                 summ / length])  # Если условия выполняются, то добавляем в маасив стартовый индекс найденной команды, длинну последовательности и summ / length
                break
            if idxs[i + 1] - idxs[
                i] > hole:  # Если следующий индекс больше текущего на 1 (означает, что следующий элемент относится уже к другой комманде)
                if (
                        length >= min_count and summ / length >= rate):  # Проверяем на условия разбора: длинна последовательности должна быть больше входного параметра min_count
                    # summ / length должно быть больше входного параметра rate
                    curr.append([curr_idx, length,
                                 summ / length])  # Если условия выполняются, то добавляем в маасив стартовый индекс найденной команды, длинну последовательности и summ / length
                curr_idx = int(idxs[i + 1])  # Изменяем текущий стартовый индекс
                summ, length = 0, 0  # Обнуляем summ и length
        curr_audio = []  # mfcc отдельной команды
        for elem in curr:  # Проходим по всему массиву curr
            # if (elem[0] != 0): # Если это не самый первый элемент исходных данных, то возьмем на одну mfcc левее (чаще всего там будет либо тишина, либо начало команды, которое не разобралось сетью)
            #  curr_audio = np.concatenate((audio_full[elem[0] - 1], audio_full[elem[0]][:, -step_mfcc:,:]), axis = 0)
            # else:
            curr_audio = audio_full[elem[0]]  # Если это стартовый элемент исходных данных, то берем самую первую mfcc
            for j in range(1, elem[
                1]):  # Пробегаем цикл от 1 до elem[1]+1 (где elem[1] хранит длинну последовательности элементов, отнесенных к одной команде)
                if (elem[0] + j == len(audio_full)):  # Если elem[0] + j равно длинне mfcc, то выходим из цикла
                    break
                # curr_audio = np.concatenate((curr_audio, audio_full[elem[0] + j][:,-step_mfcc:,:]), axis = 1) # Создаем единий mfcc, использую concatenate для добавления к текущему значению срез динной step_mfcc из следующего элемента
                curr_audio = np.hstack((curr_audio, audio_full[elem[0] + j][-step_mfcc:]))
            curr_audio = np.array(curr_audio)  # Переводим массив в numpy
            # curr_mfcc = curr_mfcc.reshape (curr_mfcc.shape[0], curr_mfcc.shape[1]) # Убираем третью размерность
            # curr_mfcc_unscaled= xScaler.inverse_transform(curr_mfcc)
            # recon = librosa.feature.inverse.mfcc_to_audio(curr_mfcc_unscaled) # Получаем ауди из mfcc
            out.append([curr_audio, idx_class, elem[2]])  # Добавляем данные в выходной массив
    return out, pred, g_pred  # Возращаем массив с данными, массив с классами команд, массив с softmax данными

# Вывод текста предсказания модели и название класса
def get_prediction_text(wavfiles, model=model, classes=CLASSES):
    result = ''
    class_name = None
    out, pred, _ = predict(wavfiles, model=model, min_count=3, rate=0.7,
                           hole=2)  # Вызываем predict для очередного файла
    if (len(out) == 0):  # Если длинна массива равна 0, то команда не распознана
        result = 'Команда не распознанана!!!'
    for elem in out:  # Пробегам по всем элементам массива out
        result = 'Распознана команда: "' + classes[elem[1]] + '" (вероятность - %.2f' % (
                elem[2] * 100) + ' %)'  # Выводим название
        class_name = classes[elem[1]]

    return result, class_name
