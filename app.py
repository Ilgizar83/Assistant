import queue
import time

import requests
import sounddevice as sd
import vosk
import json
import words
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.linear_model import LogisticRegression

from myapp import api
from skills import *
import re
import voices

# очередь для фразы произносимой
q = queue.Queue()
# модель русского языка малая
model = vosk.Model('model_small')

# sd.default.device - 1, 4  -- input, output,  т.е. указывается по умолчанию аудиовход и аудиовыход
try:
    device = sd.default.device  # <--- по умолчанию
    # или -> sd.default.device = 1, 3 или python -m sounddevice просмотр
    samplerate = int(sd.query_devices(device[0], 'input')['default_samplerate'])  # получаем частоту микрофона
except:
    voices.speaker_gtts('Включи микрофон!')
    sys.exit(1)

# регекс на триггеры
trg_regex = re.compile(r'\b%s\b' % r'\b|\b'.join(map(re.escape, words.TRIGGERS)))


# тут добавляются новые данные в контейнер
def callback(indata, frames, time, status):
    q.put(bytes(indata))


# Анализ распонзнанной речи
def recognize(data, vectorizer, clf):
    # Пропускаем все, если длина расспознанного текста меньше 7ми символов
    if len(data) < 7:
        return

    # проверяем на триггерную фразу(позвали ли ассистента)
    trg = words.TRIGGERS.intersection(data.split())
    if not trg:
        return

    # Убираем из фразы обращение к ассистенту
    data = trg_regex.sub('', data)

    # получаем вектор полученного текста
    # сравниваем с вариантами, получая наиболее подходящий ответ
    # Преобразование команды пользователя в числовой вектор
    user_command_vector = vectorizer.transform([data])
    # Предсказание вероятностей принадлежности к каждому классу
    predicted_probabilities = clf.predict_proba(user_command_vector)
    # Задание порога совпадения
    threshold = 0.10
    # Поиск наибольшей вероятности и выбор ответа, если он превышает порог
    max_probability = max(predicted_probabilities[0])
    print(max_probability)
    if max_probability >= threshold:
        answer = clf.classes_[predicted_probabilities[0].argmax()]
    else:
        voices.speaker_gtts("Команда мне не известна")
        return

    # запускаем нужную функцию
    func_name = answer.split()[0]
    voices.speaker_gtts(answer.replace(func_name, ''))
    exec(func_name + '()')


# тут мы постоянно слушаем аудиопоток
def main():
    # авторизируемся
    api.authorize()

    # из модуля words.data_set получаем ключи(образцы фраз), конвертируем в список и передоаем в метод, для создания векторов (для нахождения закономерностей)
    vectorizer = CountVectorizer()
    vectors = vectorizer.fit_transform(list(words.data_set.keys()))
    # для сопоставления вектора со значениями ключей words.data_set
    clf = LogisticRegression()
    clf.fit(vectors, list(words.data_set.values()))

    del words.data_set  # тут очищаем оперативную память

    # слушаем
    with sd.RawInputStream(samplerate=samplerate, blocksize=16000, device=device[0],
                           dtype="int16", channels=1, callback=callback):

        rec = vosk.KaldiRecognizer(model, samplerate)
        while True:
            data = q.get()
            if rec.AcceptWaveform(data):
                # тут записывается результат, получаем словарик по ключу text
                data = json.loads(rec.Result())['text']
                recognize(data, vectorizer, clf)
            # else:
            #    print(rec.PartialResult()) #тут прописывается промежуточный результат, по сути нам не нужна эта строчка     


if __name__ == '__main__':
    main()
