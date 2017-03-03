import requests
from django.conf import settings


def get_url(route_name):
    return '{0}:{1}{2}'.format(
        settings.API['default']['URL'],
        settings.API['default']['PORT'],
        settings.API['default']['ROUTES'][route_name]
    )


def post_call(url, params=None):
    if params is None:
        params = {}

    return requests.post(url, json=params)


def login(email, password):
    url = get_url('login')
    params = {"email": email, "password": password}
    response = post_call(url, params=params)

    return response.json()


def register(params):
    url = get_url('register')
    response = post_call(url, params=params)

    return response.json()
