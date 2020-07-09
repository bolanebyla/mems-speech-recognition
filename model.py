from keras.models import Sequential, model_from_json  # последовательная модель нейросети кераса
from keras.layers import Dense, Dropout, Flatten, Conv2D, MaxPooling2D, \
    BatchNormalization  # загружаем необходимые слои для нейросети

n_classes = 3  # Количество классов команд

# Cоздания модели нейросети
def get_model():
    model = Sequential()
    model.add(Conv2D(8, kernel_size=(3, 3), activation='relu', input_shape=(20, 22, channel)))
    model.add(
        MaxPooling2D(pool_size=(2, 2)))  # передаём на слой подвыборки, снижающий размерность поступивших на него данных
    model.add(BatchNormalization())  # пропускаем через слой нормализации данных
    model.add(Flatten())  # сплющиваем в одномерный вектор
    model.add(Dense(128, activation='relu'))  # добавляем полносвязный слой размером в заданное кол-во нейронов
    model.add(Dropout(
        0.25))  # добавляем слой регуляризации, "выключая" указанное количество нейронов, во избежание переобучения
    model.add(BatchNormalization())  # пропускаем через слой нормализации данных
    model.add(Dense(n_classes,
                    activation='softmax'))  # добавляем полносвязный слой с функцией активации softmax на выходном слое для 3 классов
    model.compile(loss='categorical_crossentropy',
                  optimizer='Adam',
                  metrics=[
                      'accuracy'])  # компилируем, составляем модель с алгоритмом оптимизации, функцией потерь и метрикой точности

    # Сохранение модели в json
    with open('model-mem.json', 'w') as f:
        f.write(model.to_json())

    return model

# model = get_model()
# model.load_weights("model-cnn.h5")
