import requests
from django.conf import settings


def get_url(route_name):
    return '{0}:{1}/{2}'.format(
        settings.API['default']['URL'],
        settings.API['default']['PORT'],
        settings.API['default']['ROUTES'][route_name]
    )


def call(url, params=None):
    if params is None:
        params = {}

    return requests.get(url, params=params)


def login(email, password):
    url = get_url('login')
    params = {'email': email, 'password': password}
    response = call(url, params)
    # books = response.json()
    # return {'books':books['results']}
