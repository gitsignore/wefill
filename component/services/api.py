import requests
from django.conf import settings
from django.urls import reverse
from app.exceptions import RedirectException


def header_token(token):
    """
    Set token in header
    :param token:
    :return Dict:
    """
    return {'Authorization': '{0} {1}'.format('JWT', token)}


def get_url(route_name, param=''):
    """
    Build api url with optionnal param
    :param route_name:
    :param param:
    :return string:
    """
    return '{0}:{1}{2}{3}'.format(
        settings.API['default']['URL'],
        settings.API['default']['PORT'],
        settings.API['default']['ROUTES'][route_name],
        param
    )


def get_call(url, params=None, headers=None):
    """
    Call api with GET method
    :param url:
    :param params:
    :param headers:
    :return:
    """
    response = requests.get(url, params=params, headers=headers)

    if response.status_code == 401:
        raise RedirectException(reverse('logout'))

    return response


def post_call(url, params=None, json=None, headers=None):
    """
    Call api with POST method
    :param url:
    :param params:
    :param json:
    :param headers:
    :return:
    """
    if params is None:
        params = {}

    response = requests.post(url, data=params, json=json, headers=headers)

    if response.status_code == 401:
        raise RedirectException(reverse('logout'))

    return response


def put_call(url, params=None, json=None, headers=None):
    """
    Call api with PUT method
    :param url:
    :param params:
    :param json:
    :param headers:
    :return:
    """
    if params is None:
        params = {}

    if json is None:
        json = {}

    response = requests.put(url, params=params, json=json, headers=headers)

    if response.status_code == 401:
        raise RedirectException(reverse('logout'))

    return response


def delete_call(url, headers=None):
    """
    Call api with DELETE method
    :param url:
    :param headers:
    :return:
    """
    response = requests.delete(url, headers=headers)

    if response.status_code == 401:
        raise RedirectException(reverse('logout'))

    return response


def login(params):
    """
    Login user
    :param params:
    :return:
    """
    url = get_url('login')

    return post_call(url, json=params)


def register(params):
    """
    Register user
    :param params:
    :return:
    """
    url = get_url('users')

    return post_call(url, json=params)


def get_user(user_email, token):
    """
    Retrieve user
    :param user_email:
    :param token:
    :return:
    """
    url = get_url('users', user_email)
    headers = header_token(token)

    return get_call(url, headers=headers)


def edit_user(user, token):
    """
    Edit user
    :param user:
    :param token:
    :return:
    """
    url = get_url('users', user['email'] + '/')
    headers = header_token(token)

    return put_call(url, json=user, headers=headers)


def get_address(address_id, token):
    """
    Retieve user address
    :param address_id:
    :param token:
    :return:
    """
    url = get_url('addresses', address_id)
    headers = header_token(token)

    return get_call(url, headers=headers)


def create_address(address, token):
    """
    Create user address
    :param address:
    :param token:
    :return:
    """
    url = get_url('addresses')
    headers = header_token(token)

    return post_call(url, json=address, headers=headers)


def edit_address(address, token):
    """
    Edit user address
    :param address:
    :param token:
    :return:
    """
    url = get_url('addresses', address['id'] + '/')
    headers = header_token(token)

    return put_call(url, json=address, headers=headers)


def delete_address(address_id, token):
    """
    Delete user address
    :param address_id:
    :param token:
    :return:
    """
    url = get_url('addresses', address_id)
    headers = header_token(token)

    return delete_call(url, headers=headers)


def get_vehicle(vehicle_id, token):
    """
    Retrieve user vehicle
    :param vehicle_id:
    :param token:
    :return:
    """
    url = get_url('vehicles', vehicle_id)
    headers = header_token(token)

    return get_call(url, headers=headers)


def create_vehicle(vehicle, token):
    """
    Create user vehicle
    :param vehicle:
    :param token:
    :return:
    """
    url = get_url('vehicles')
    headers = header_token(token)

    return post_call(url, json=vehicle, headers=headers)


def edit_vehicle(vehicle, token):
    """
    Edit user vehicle
    :param vehicle:
    :param token:
    :return:
    """
    url = get_url('vehicles', vehicle['id'] + '/')
    headers = header_token(token)

    return put_call(url, json=vehicle, headers=headers)


def delete_vehicle(vehicle_id, token):
    """
    Delete user vehicle
    :param vehicle_id:
    :param token:
    :return:
    """
    url = get_url('vehicles', vehicle_id)
    headers = header_token(token)

    return delete_call(url, headers=headers)


def order_validate(order, token):
    """
    Create an order
    :param order:
    :param token:
    :return:
    """
    url = get_url('orders')
    headers = header_token(token)

    return post_call(url, json=order, headers=headers)


def order_update(order, token):
    """
    Update an order
    :param order:
    :param token:
    :return:
    """
    url = get_url('orders', str(order['id']) + '/')
    headers = header_token(token)

    return put_call(url, json=order, headers=headers)


def get_gas(token):
    """
    Get gas choices
    :param token:
    :return:
    """
    url = get_url('gas')
    headers = header_token(token)

    return get_call(url, headers=headers)


def get_gas_by_id(gas_id, token):
    """
    Get gas by id
    :param token:
    :return:
    """
    url = get_url('gas', gas_id)
    headers = header_token(token)

    return get_call(url, headers=headers)


def create_gas(gas, token):
    """
    Create gas
    :param gas:
    :param token:
    :return:
    """
    url = get_url('gas')
    headers = header_token(token)

    return post_call(url, json=gas, headers=headers)


def edit_gas(gas, token):
    """
    Edit gas
    :param gas:
    :param token:
    :return:
    """
    url = get_url('gas', gas['id'])
    headers = header_token(token)

    return put_call(url, json=gas, headers=headers)


def delete_gas(gas_id, token):
    """
    Delete gas
    :param gas_id:
    :param token:
    :return:
    """
    url = get_url('gas', gas_id)
    headers = header_token(token)

    return delete_call(url, headers=headers)


def get_order(id, token):
    url = get_url('orders', id)
    headers = header_token(token)

    return get_call(url, headers=headers)


def get_orders(token, start_date=None, end_date=None):
    query_params = ''
    if start_date:
        query_params += 'start_date=' + start_date
    if end_date:
        if len(query_params) < 1:
            query_params += '?'
        else:
            query_params += '&'
        query_params += 'end_date=' + end_date

    url = get_url('orders')
    headers = header_token(token)

    return get_call(url, params=query_params, headers=headers)
