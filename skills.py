import os, webbrowser, sys, requests, subprocess

from myapp import api, voices
from myapp.voices import speaker_silero, speaker_gtts


def browser():
    # открывает браузер заданнный по умолчанию в системе с url указанным здесь
    webbrowser.open('https://www.youtube.com', new=2)


def game():
    # размещаем путь к exe файлу любого приложения или игры, для запуска по команде
    subprocess.Popen('C:\Windows\System32\calc.exe')


def offpc():
    # эта команда отключает ПК под управлением Windows
    os.system('shutdown \s')


def weather():
    # авторизируемся на сайте https://openweathermap.org для получения информации о погоде
    try:
        params = {'q': 'Kazan', 'units': 'metric', 'lang': 'ru', 'appid': '*************'}      # чтобы заработало надо изменить appid
        response = requests.get(f'https://api.openweathermap.org/data/2.5/weather', params=params)
        if not response:
            raise
        w = response.json()
        speaker_gtts(f"На улице {w['weather'][0]['description']} {round(w['main']['temp'])} градусов")

    except:
        speaker_gtts('Произошла ошибка при попытке запроса к ресурсу API, проверь код')


def offBot():
    # команда отключает бота
    sys.exit()


def passive():
    # функция заглушка при простом диалоге с ботом
    pass


def lighton():
    # включаем подсветку логотипа
    uuid = '***********************'          # нужно указать uuid параметра
    response = api.change_param(uuid, '1')
    print(response)
    if response == 200:
        voices.speaker_gtts('Сделано')
    else:
        voices.speaker_gtts('Сделал кажется что-то не то')


def lightoff():
    # включаем подсветку
    uuid = '***********************'        # нужно указать uuid параметра
    response = api.change_param(uuid, '2')
    print(response)
    if response == 200:
        voices.speaker_gtts('Готово')
    else:
        voices.speaker_gtts('Сделал кажется что-то не то')


def lightinfo():
    # включаем подсветку
    uuid = '***********************'        # нужно указать uuid параметра
    response = api.get_param(uuid)
    print(response)
    if response == '1':
        voices.speaker_gtts('Логотип включен')
    elif response == '2':
        voices.speaker_gtts('Логотип выключен')
    else:
        voices.speaker_gtts('Что то не понятное у нее значение ')


def venton():
    # включаем приточно-вытяжную систему в ЕДЦ
    uuid = '*************************'      # нужно указать uuid параметра
    response = api.change_param(uuid, '76')
    print(response)
    if response == 200:
        voices.speaker_gtts('Выполнено')
    else:
        voices.speaker_gtts('Сделал кажется что-то не то')


def ventoff():
    # отключаем приточно-вытяжную систему в ЕДЦ
    uuid = '*************************'      # нужно указать uuid параметра
    response = api.change_param(uuid, '6')
    print(response)
    if response == 200:
        voices.speaker_gtts('Сделано')
    else:
        voices.speaker_gtts('Сделал кажется что-то не то')


def ventinfo():
    # получаем статус работы приточно-вытяжной системы в ЕДЦ
    uuid = '*************************'      # нужно указать uuid параметра
    response = api.get_param(uuid)
    print(response)
    if response == '76' or response == '70':
        voices.speaker_gtts('Тепловой насос включен')
    elif response == '6' or response == '12':
        voices.speaker_gtts('Тепловой насос выключен')
    else:
        voices.speaker_gtts('Что то не понятное у него значение ')
