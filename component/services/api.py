import requests
from django.conf import settings


def header_token(token):
    return {'Authorization': '{0} {1}'.format('JWT', token)}


def get_url(route_name, param=''):
    return '{0}:{1}{2}{3}'.format(
        settings.API['default']['URL'],
        settings.API['default']['PORT'],
        settings.API['default']['ROUTES'][route_name],
        param
    )


def get_call(url, params=None, headers=None):
    return requests.get(url, params=params, headers=headers)


def post_call(url, params=None, json=None):
    if params is None:
        params = {}

    return requests.post(url, data=params, json=json)


def login(params):
    url = get_url('login')
    response = post_call(url, params=params)

    return response.json()


def register(params):
    url = get_url('users')
    response = post_call(url, params=params)

    return response.json()


def account_informations(user_email, token):
    url = get_url('users', user_email)
    headers = header_token(token)
    response = get_call(url, headers=headers)

    return response.json()
