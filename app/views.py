# -*- coding: utf-8 -*-
import calendar as cal
from django.conf import settings
from calendar import calendar
from datetime import date, datetime
from django.contrib import messages
from django.shortcuts import render
from app.decorators import auth_required, admin_required
from app.forms import LoginForm, RegisterForm, ProfileForm, AddressForm, VehicleForm, GasForm, OrderForm
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from component.services.api import login as api_login
from component.services.api import register as api_register
from component.services.api import get_user as api_get_user
from component.services.api import edit_user as api_edit_user
from component.services.api import get_address as api_get_address
from component.services.api import get_vehicle as api_get_vehicle
from component.services.api import create_address as api_create_address
from component.services.api import create_vehicle as api_create_vehicle
from component.services.api import edit_address as api_edit_address
from component.services.api import edit_vehicle as api_edit_vehicle
from component.services.api import delete_address as api_delete_address
from component.services.api import delete_vehicle as api_delete_vehicle
from component.services.api import order_validate as api_order_validate
from component.services.api import order_update as api_order_update
from component.services.api import get_gas as api_get_gas
from component.services.api import get_gas_by_id as api_get_gas_by_id
from component.services.api import create_gas as api_create_gas
from component.services.api import edit_gas as api_edit_gas
from component.services.api import delete_gas as api_delete_gas
from component.services.api import get_orders as api_get_orders
from component.services.api import get_order as api_get_order
from component.services.paypal_api import build_params as paypal_build_params
from paypal.standard.forms import PayPalPaymentsForm


def login(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            response = api_login(form.cleaned_data)
            if response.ok:
                user = response.json()
                request.session['user'] = user
                request.session['is_authenticated'] = True
                if 'is_admin' in user:
                    request.session['is_admin'] = user['is_admin']

                return HttpResponseRedirect(reverse('wefill'))

            return render(request, 'registration/login.html',
                          {'form': form, 'errors': response.json()['errors']['non_field_errors']})
    else:
        form = LoginForm()

    return render(request, 'registration/login.html', {'form': form})


def register(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            form.cleaned_data['username'] = form.cleaned_data['email']
            response = api_register(form.cleaned_data)
            if response.ok:
                user = response.json()
                request.session['user'] = user
                request.session['is_authenticated'] = True
                if 'is_admin' in user:
                    request.session['is_admin'] = user['is_admin']

                return HttpResponseRedirect(reverse('wefill'))
            return render(request, 'registration/register.html', {
                'form': form, 'errors': response.json()['errors']
            })
    else:
        form = RegisterForm()

    return render(request, 'registration/register.html', {'form': form})


def logout(request):
    try:
        del request.session['user']
        del request.session['order']
        del request.session['is_authenticated']
        del request.session['is_admin']
    except KeyError:
        pass
    return HttpResponseRedirect(reverse('wefill'))


@auth_required
def profile(request):
    response = api_get_user(request.session['user']['email'], request.session['user']['token'])

    if response.ok:
        return render(request, 'profile.html', {'user': response.json()})
    return HttpResponseRedirect(reverse('logout'))


@auth_required
def edit_profile(request):
    response = api_get_user(request.session['user']['email'], request.session['user']['token'])
    if response.ok:
        user = response.json()
        if request.method == 'POST':
            form = ProfileForm(request.POST)
            if form.is_valid():
                data = form.cleaned_data
                user['lastname'] = data['lastname']
                user['firstname'] = data['firstname']
                user.pop('order_set')
                user.pop('address_set')
                user.pop('vehicle_set')
                response = api_edit_user(user, request.session['user']['token'])
                if response.ok:
                    return HttpResponseRedirect(reverse('profile'))
                return render(request, 'profile/edit.html', {
                    'form': form, 'errors': response.json()['errors']
                })

        form = ProfileForm(initial=user)
        return render(request, 'profile/edit.html', {'form': form})
    return HttpResponseRedirect(reverse('logout'))


@auth_required
def create_address(request):
    if request.method == 'POST':
        form = AddressForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            data['user'] = request.session['user']['id']
            response = api_create_address(data, request.session['user']['token'])
            if response.ok:
                return HttpResponseRedirect(reverse('profile'))
            return render(request, 'address/create_address.html', {
                'form': form, 'errors': response.json()['errors']
            })
    else:
        form = AddressForm()

    return render(request, 'address/create_address.html', {'form': form})


@auth_required
def edit_address(request, address_id):
    response = api_get_address(address_id, request.session['user']['token'])
    if response.ok:
        address = response.json()
        if request.method == 'POST':
            form = AddressForm(request.POST)
            if form.is_valid():
                data = form.cleaned_data
                data['user'] = request.session['user']['id']
                data['id'] = str(response.json()['id'])
                response = api_edit_address(data, request.session['user']['token'])
                if response.ok:
                    return HttpResponseRedirect(reverse('profile'))
                return render(request, 'address/edit_address.html', {
                    'form': form, 'errors': response.json()['errors'], 'id': address_id
                })
        else:
            form = AddressForm(initial=address)

        return render(request, 'address/edit_address.html', {'form': form, 'id': address_id})
    return HttpResponseRedirect(reverse('profile'))


@auth_required
def delete_address(request, address_id):
    api_delete_address(address_id, request.session['user']['token'])

    return HttpResponseRedirect(reverse('profile'))


@auth_required
def create_vehicle(request):
    if request.method == 'POST':
        form = VehicleForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            data['user'] = request.session['user']['id']
            response = api_create_vehicle(data, request.session['user']['token'])
            if response.ok:
                return HttpResponseRedirect(reverse('profile'))
            return render(request, 'vehicle/create_vehicle.html', {
                'form': form, 'errors': response.json()['errors']
            })
    else:
        form = VehicleForm()

    return render(request, 'vehicle/create_vehicle.html', {'form': form})


@auth_required
def edit_vehicle(request, vehicle_id):
    response = api_get_vehicle(vehicle_id, request.session['user']['token'])

    if response.ok:
        vehicle = response.json()
        if request.method == 'POST':
            form = VehicleForm(request.POST)
            if form.is_valid():
                data = form.cleaned_data
                data['user'] = request.session['user']['id']
                data['id'] = str(response.json()['id'])
                response = api_edit_vehicle(data, request.session['user']['token'])
                if response.ok:
                    return HttpResponseRedirect(reverse('profile'))
                return render(request, 'vehicle/edit_vehicle.html', {
                    'form': form, 'errors': response.json()['errors']
                })
        else:
            form = VehicleForm(initial=vehicle)

        return render(request, 'vehicle/edit_vehicle.html', {'form': form, 'id': vehicle_id})
    return HttpResponseRedirect(reverse('profile'))


@auth_required
def delete_vehicle(request, vehicle_id):
    api_delete_vehicle(vehicle_id, request.session['user']['token'])

    return HttpResponseRedirect(reverse('profile'))


@auth_required
@admin_required
def admin(request):
    today = date.today()
    gas_response = api_get_gas(request.session['user']['token'])
    order_response = api_get_orders(request.session['user']['token'], str(today), str(today))

    if gas_response.ok and order_response.ok:
        order_response = order_response.json()
        for index, order in enumerate(order_response):
            order_response[index]['date_refill'] = datetime.strptime(order['date_refill'], '%Y-%m-%dT%H:%M:%SZ')
        return render(request, 'admin.html', {'gas': gas_response.json(), 'orders': order_response})
    return HttpResponseRedirect(reverse('wefill'))


@auth_required
@admin_required
def create_gas(request):
    if request.method == 'POST':
        form = GasForm(request.POST)
        if form.is_valid():
            response = api_create_gas(form.cleaned_data, request.session['user']['token'])
            if response.ok:
                return HttpResponseRedirect(reverse('gas'))
            return render(request, 'gas/create_gas.html', {
                'form': form, 'errors': response.json()['errors']
            })
    else:
        form = GasForm()

    return render(request, 'gas/create_gas.html', {'form': form})


@auth_required
@admin_required
def edit_gas(request, gas_id):
    response = api_get_gas_by_id(gas_id, request.session['user']['token'])

    if response.ok:
        gas = response.json()
        if request.method == 'POST':
            form = GasForm(request.POST)
            if form.is_valid():
                response = api_edit_gas(form.cleaned_data, request.session['user']['token'])
                if response.ok:
                    return HttpResponseRedirect(reverse('gas'))
                return render(request, 'gas/edit_gas.html', {
                    'form': form, 'errors': response.json()['errors']
                })
        else:
            form = GasForm(initial=gas)

        return render(request, 'gas/edit_gas.html', {'id': gas['id'], 'form': form})
    return HttpResponseRedirect(reverse('gas'))


@auth_required
@admin_required
def delete_gas(request, gas_id):
    api_delete_gas(gas_id, request.session['user']['token'])

    return HttpResponseRedirect(reverse('gas'))


@auth_required
def orders(request):
    response = api_get_orders(request.session['user']['token'])

    if response.ok:
        orders = response.json()
        for index, order in enumerate(orders):
            orders[index]['date_refill'] = datetime.strptime(order['date_refill'], '%Y-%m-%dT%H:%M:%SZ')
        return render(request, 'orders.html', {'orders': orders})
    return HttpResponseRedirect(reverse('logout'))


@auth_required
def book(request):
    token = request.session['user']['token']
    user_response = api_get_user(request.session['user']['email'], token)
    gas_choices_response = api_get_gas(request.session['user']['token'])
    if user_response.ok and gas_choices_response.ok:
        user = user_response.json()
        if not user['address_set']:
            messages.warning(request, 'Vous devez créer une adresse.')
            return HttpResponseRedirect(reverse('create_address'))
        if not user['vehicle_set']:
            messages.warning(request, 'Vous devez ajouter un véhicule.')
            return HttpResponseRedirect(reverse('create_vehicle'))
        gas_choices = gas_choices_response.json()
        if request.method == 'POST':
            form = OrderForm(request.POST, user['address_set'], user['vehicle_set'], gas_choices)
            if form.is_valid():
                data = form.cleaned_data
                if int(data['date_refill'].month) > int(date.today().month) + settings.CALENDAR['months_visibilty']:
                    return render(request, 'book.html', {
                        'form': form, 'errors': 'Date invalide'
                    })
                data['user'] = request.session['user']['id']
                for gas_choice in gas_choices:
                    if data['gas_name'] == gas_choice['name']:
                        data.update({'gas_price': gas_choice['price']})
                        break
                order_response = api_order_validate(data, request.session['user']['token'])
                if order_response.ok:
                    request.session['order'] = order_response.json()
                    request.session['payment'] = True
                    return HttpResponseRedirect(reverse('payment'))
                return render(request, 'book.html', {
                    'form': form, 'errors': order_response.json()['errors']
                })

        form = OrderForm(None, user['address_set'], user['vehicle_set'], gas_choices)

        return render(request, "book.html", {
            'user': user,
            'form': form,
        })
    return HttpResponseRedirect(reverse('logout'))


@auth_required
def payment(request):
    try:
        order_response = api_get_order(request.session['order']['id'], request.session['user']['token'])
        user = request.session['user']

        if order_response.ok and user:
            order = order_response.json()
            paypal_dict = paypal_build_params(order, user)

            form = PayPalPaymentsForm(initial=paypal_dict)
            context = {'form': form, 'order': order, 'amount': order['gas_quantity'] * order['gas_price']}
            request.session['order'] = order

            return render(request, "payment.html", context)
    except KeyError:
        return HttpResponseRedirect(reverse('book'))
    return HttpResponseRedirect(reverse('book'))


@auth_required
def summary(request):
    # Hook to simulate paypal callback
    try:
        order_response = api_get_order(request.session['order']['id'], request.session['user']['token'])
        user = request.session['user']

        if order_response.ok and user:
            order = order_response.json()
            order['is_payed'] = True
            api_order_update(order, request.session['user']['token'])

            context = {'order': order}
            del request.session['order']

            return render(request, "summary.html", context)
    except KeyError:
        return HttpResponseRedirect(reverse('book'))
    return HttpResponseRedirect(reverse('book'))


@auth_required
def calendar(request, year, month):
    """
    Show calendar of events for a given month of a given year.
    """
    token = request.session['user']['token']
    today = date.today()
    monthrange = cal.monthrange(int(year), int(month))
    month = '%02d' % int(month)
    date_start = year + '-' + month + '-' + '01'
    date_end = year + '-' + month + '-' + str(monthrange[1])
    response = api_get_orders(token, date_start, date_end)
    orders = response.json()
    my_year = int(year)
    my_month = int(month)

    if my_month < int(today.month) or my_year < int(today.year):
        my_month = int(today.month)
        my_year = int(today.year)

    max_month = int(today.month) + settings.CALENDAR['months_visibilty']

    if my_month > max_month:
        my_month = max_month

    # Calculate values for the calendar controls. 1-indexed (Jan = 1)
    my_previous_year = my_year
    if today.month < my_month:
        my_previous_month = my_month - 1
        if my_previous_month == 0:
            my_previous_year = my_year - 1
            my_previous_month = 12
    else:
        my_previous_year = ''
        my_previous_month = ''
    if max_month > my_month:
        my_next_year = my_year
        my_next_month = my_month + 1
        if my_next_month == 13:
            my_next_year = my_year + 1
            my_next_month = 1
    else:
        my_next_year = ''
        my_next_month = ''
    my_year_after_this = my_year + 1
    my_year_before_this = my_year - 1

    return render(request, "calendar/calendar.html", {
        'event_list': orders,
        'month': my_month,
        'month_name': named_month(my_month),
        'year': my_year,
        'previous_month': my_previous_month,
        'previous_month_name': named_month(my_previous_month),
        'previous_year': my_previous_year,
        'next_month': my_next_month,
        'next_month_name': named_month(my_next_month),
        'next_year': my_next_year,
        'year_before_this': my_year_before_this,
        'year_after_this': my_year_after_this,
    })


def named_month(month_number):
    """
    Return the name of the month, given the number.
    """
    if month_number != '':
        return date(1900, month_number, 1).strftime("%B")
    else:
        return ''


def this_month(request):
    """
    Show calendar of events this month.
    """
    today = datetime.now()
    return calendar(request, today.year, today.month)
