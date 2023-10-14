import os, webbrowser, sys, requests, subprocess

from myapp import api, voices
from myapp.voices import speaker_silero, speaker_gtts


def browser():
    # Открывает браузер заданнный по уполчанию в системе с url указанным здесь
    webbrowser.open('https://www.youtube.com', new=2)


def game():
    subprocess.Popen('C:\Windows\System32\calc.exe')  # Нужно разместить путь к exe файлу любого вашего приложения


def offpc():
    # Эта команда отключает ПК под управлением Windows
    os.system('shutdown \s')


# print('пк был бы выключен, но команде # в коде мешает;)))')

def weather():
    # Для работы этого кода нужно зарегистрироваться на сайте https://openweathermap.org или переделать на ваше усмотрение под что-то другое
    try:
        params = {'q': 'Kazan', 'units': 'metric', 'lang': 'ru', 'appid': '08a14fa0243d698514bc9879f886c9b4'}
        response = requests.get(f'https://api.openweathermap.org/data/2.5/weather', params=params)
        if not response:
            raise
        w = response.json()
        speaker_gtts(f"На улице {w['weather'][0]['description']} {round(w['main']['temp'])} градусов")

    except:
        speaker_gtts('Произошла ошибка при попытке запроса к ресурсу API, проверь код')


def offBot():
    # Отключает бота
    sys.exit()


def passive():
    # Функция заглушка при простом диалоге с ботом
    pass


def lighton():
    # включаем подсветку
    # Подкорректировать гуид
    uuid = '03a7e3ec-9142-496e-94e0-95179889fdb2'
    response = api.change_param(uuid, '1')
    print(response)
    if response == 200:
        voices.speaker_gtts('Сделано')
    else:
        voices.speaker_gtts('Сделал кажется что-то не то')


def lightoff():
    # включаем подсветку
    # Подкорректировать гуид
    uuid = '03a7e3ec-9142-496e-94e0-95179889fdb2'
    response = api.change_param(uuid, '2')
    print(response)
    if response == 200:
        voices.speaker_gtts('Готово')
    else:
        voices.speaker_gtts('Сделал кажется что-то не то')


def lightinfo():
    # включаем подсветку
    # Подкорректировать гуид
    uuid = '03a7e3ec-9142-496e-94e0-95179889fdb2'
    response = api.get_param(uuid)
    print(response)
    if response == '1':
        voices.speaker_gtts('Логотип включен')
    elif response == '2':
        voices.speaker_gtts('Логотип выключен')
    else:
        voices.speaker_gtts('Что то не понятное у нее значение ')


def venton():
    uuid = '8ecb3d59-005b-483a-91af-481dd10966ad'
    response = api.change_param(uuid, '76')
    print(response)
    if response == 200:
        voices.speaker_gtts('Выполнено')
    else:
        voices.speaker_gtts('Сделал кажется что-то не то')


def ventoff():
    uuid = '8ecb3d59-005b-483a-91af-481dd10966ad'
    response = api.change_param(uuid, '6')
    print(response)
    if response == 200:
        voices.speaker_gtts('Сделано')
    else:
        voices.speaker_gtts('Сделал кажется что-то не то')


def ventinfo():
    # Подкорректировать гуид
    uuid = '8ecb3d59-005b-483a-91af-481dd10966ad'
    response = api.get_param(uuid)
    print(response)
    if response == '76' or response == '70':
        voices.speaker_gtts('Тепловой насос включен')
    elif response == '6' or response == '12':
        voices.speaker_gtts('Тепловой насос выключен')
    else:
        voices.speaker_gtts('Что то не понятное у него значение ')
