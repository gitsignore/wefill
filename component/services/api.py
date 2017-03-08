import requests
from django.conf import settings
from django.urls import reverse
from app.exceptions import RedirectException


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
    response = requests.get(url, params=params, headers=headers)

    if response.status_code == 401:
        raise RedirectException(reverse('logout'))

    if 200 <= response.status_code < 400:
        return response.json()

    return False


def post_call(url, params=None, json=None, headers=None):
    if params is None:
        params = {}

    response = requests.post(url, data=params, json=json, headers=headers)

    if response.status_code == 401:
        raise RedirectException(reverse('logout'))

    if 200 <= response.status_code < 400:
        return response.json()

    return False


def login(params):
    url = get_url('login')

    return post_call(url, params=params)


def register(params):
    url = get_url('users')

    return post_call(url, params=params)


def get_user(user_email, token):
    url = get_url('users', user_email)
    headers = header_token(token)

    return get_call(url, headers=headers)


def get_address(address_id, token):
    url = get_url('addresses', address_id)
    headers = header_token(token)

    return get_call(url, headers=headers)


def edit_address(address, token):
    url = get_url('addresses')
    headers = header_token(token)

    return post_call(url, params=address, headers=headers)


def get_vehicle(vehicle_id, token):
    url = get_url('vehicles', vehicle_id)
    headers = header_token(token)

    return get_call(url, headers=headers)


def edit_vehicle(vehicle, token):
    url = get_url('vehicles')
    headers = header_token(token)

    return post_call(url, params=vehicle, headers=headers)
