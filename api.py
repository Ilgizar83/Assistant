import requests
import time

serv_access_token = None
serv_refresh_token = None
access_token = None
token_exp = None
refresh_token = None
url = '*****************'
project_uuid = "************"

routes = [
    '/api/sign-in',
    '/api/refresh-token',
    '/api/parameter/value',
    '/api/parameter/{}',
    '/api/server-sign-in'
]


def auth_serv(login='*****', password='*****'):
    try:
        response = requests.post(url + routes[4],
                                 json={'login': login, 'password': password, 'projectUuid': project_uuid})
        response.raise_for_status()
    except Exception as e:
        raise e
    else:
        global serv_access_token, serv_refresh_token
        serv_access_token = response.json()['access_token']
        serv_refresh_token = response.json()['refresh_token']


def authorize(login='*******', password='*******'):
    global serv_access_token
    try:
        auth_serv()
        if not serv_access_token:
            print('Не получен серверный токен')
    except Exception as e:
        raise e

    try:
        response = requests.post(url + routes[0], headers={'Authorization': serv_access_token},
                                 json={'login': login, 'password': password, 'projectUuid': project_uuid})
        response.raise_for_status()
    except Exception as e:
        raise e
    else:
        global access_token, refresh_token, token_exp
        access_token = response.json()['access_token']
        refresh_token = response.json()['refresh_token']
        token_exp = time.time() + 20 * 60


def refresh_access():
    global access_token, refresh_token, token_exp
    try:
        response = requests.post(url + routes[1], json={'refresh_token': refresh_token})
        response.raise_for_status()
    except Exception as e:
        raise e
    else:
        access_token = response.json()['access_token']
        refresh_token = response.json()['refresh_token']
        token_exp = time.time() + 20 * 60
        return None


def renew_access_token(func):
    def wrapper(*args, **kwargs):
        if time.time() >= token_exp:
            refresh_access()
        return func(*args, **kwargs)

    return wrapper


@renew_access_token
def get_param(uuid):
    try:
        response = requests.get((url + routes[3]).format(uuid), headers={'Authorization': access_token})
        response.raise_for_status()
    except Exception as e:
        raise e
    else:
        return response.json()['value']


@renew_access_token
def change_param(uuid, value):
    try:
        response = requests.post(url + routes[2], headers={'Authorization': access_token},
                                 json={'parameterUuid': uuid, 'value': value})
        response.raise_for_status()
    except Exception as e:
        raise e
    else:
        return response.status_code
