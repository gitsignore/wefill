from calendar import calendar
from datetime import date, datetime
from django.shortcuts import render
from app.decorators import auth_required
from app.forms import LoginForm, RegisterForm, AddressForm, VehicleForm, OrderForm
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from component.services.api import login as api_login
from component.services.api import register as api_register
from component.services.api import get_user as api_get_user
from component.services.api import get_address as api_get_address
from component.services.api import get_vehicle as api_get_vehicle
from component.services.api import create_address as api_create_address
from component.services.api import create_vehicle as api_create_vehicle
from component.services.api import edit_address as api_edit_address
from component.services.api import edit_vehicle as api_edit_vehicle
from component.services.api import order_validate as api_order_validate
from component.services.api import get_gas as api_get_gas
from component.services.api import get_orders as api_get_orders
from component.services.api import get_order as api_get_order

from component.services.paypal_api import build_params as paypal_build_params

from paypal.standard.forms import PayPalPaymentsForm


def login(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            user = api_login(form.cleaned_data)
            if user:
                request.session['user'] = user
                request.session['is_authenticated'] = True
                if 'is_admin' in user:
                    request.session['is_admin'] = user['is_admin']

                return HttpResponseRedirect(reverse('wefill'))

            return render(request, 'registration/login.html',
                          {'form': form, 'errors': user['non_field_errors']})
    else:
        form = LoginForm()

    return render(request, 'registration/login.html', {'form': form})


def register(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            form.cleaned_data['username'] = form.cleaned_data['email']
            user = api_register(form.cleaned_data)
            if user:
                request.session['user'] = user
                request.session['is_authenticated'] = True
                if 'is_admin' in user:
                    request.session['is_admin'] = user['is_admin']

                return HttpResponseRedirect(reverse('wefill'))
            return render(request, 'registration/register.html', {
                'form': form, 'errors': user['errors']
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
    user = api_get_user(request.session['user']['email'], request.session['user']['token'])

    return render(request, 'profile.html', {'user': user})


@auth_required
def create_address(request):
    if request.method == 'POST':
        form = AddressForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            data['user'] = request.session['user']['id']
            address = api_create_address(data, request.session['user']['token'])
            if address:
                return HttpResponseRedirect(reverse('profile'))
            return render(request, 'address/create_address.html', {
                'form': form, 'errors': address['errors']
            })
    else:
        form = AddressForm()

    return render(request, 'address/create_address.html', {'form': form})


@auth_required
def edit_address(request, address_id):
    address = api_get_address(address_id, request.session['user']['token'])
    if request.method == 'POST':
        form = AddressForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            data['user'] = request.session['user']['id']
            address = api_edit_address(data, request.session['user']['token'])
            if address:
                return HttpResponseRedirect(reverse('profile'))
            return render(request, 'address/edit_address.html', {
                'form': form, 'errors': address['errors'], 'id': address['id']
            })
    else:
        form = AddressForm(initial=address)

    return render(request, 'address/edit_address.html', {'form': form, 'id': address['id']})


@auth_required
def create_vehicle(request):
    if request.method == 'POST':
        form = VehicleForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            data['user'] = request.session['user']['id']
            vehicle = api_create_vehicle(data, request.session['user']['token'])
            if vehicle:
                return HttpResponseRedirect(reverse('profile'))
            return render(request, 'vehicle/create_vehicle.html', {
                'form': form, 'errors': vehicle['errors']
            })
    else:
        form = VehicleForm()

    return render(request, 'vehicle/create_vehicle.html', {'form': form})


@auth_required
def edit_vehicle(request, vehicle_id):
    vehicle = api_get_vehicle(vehicle_id, request.session['user']['token'])
    if request.method == 'POST':
        form = VehicleForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            data['user'] = request.session['user']['id']
            vehicle = api_edit_vehicle(data, request.session['user']['token'])
            if vehicle:
                return HttpResponseRedirect(reverse('profile'))
            return render(request, 'vehicle/edit_vehicle.html', {
                'form': form, 'errors': vehicle['errors']
            })
    else:
        form = VehicleForm(initial=vehicle)

    return render(request, 'vehicle/edit_vehicle.html', {'form': form})


@auth_required
def orders(request):
    orders = api_get_orders(request.session['user']['token'])

    return render(request, 'orders.html', {'orders': orders})


@auth_required
def book(request):
    """
        Show calendar of events for a given month of a given year.
        ``series_id``
        The event series to show. None shows all event series.

        """
    token = request.session['user']['token']
    user = api_get_user(request.session['user']['email'], token)
    gas_choices = api_get_gas(request.session['user']['token'])
    if request.method == 'POST':
        form = OrderForm(request.POST, user['address_set'], user['vehicle_set'], gas_choices)
        if form.is_valid():
            data = form.cleaned_data
            data['user'] = request.session['user']['id']
            for gas_choice in gas_choices:
                if data['gas_name'] == gas_choice['name']:
                    data.update({'gas_price': gas_choice['price']})
            order = api_order_validate(data, request.session['user']['token'])
            if order:
                request.session['order'] = order
                request.session['payment'] = True
                return HttpResponseRedirect(reverse('payment'))
            return render(request, 'book.html', {
                'form': form, 'errors': order['errors']
            })

    form = OrderForm(None, user['address_set'], user['vehicle_set'], gas_choices)

    return render(request, "book.html", {
        'user': user,
        'form': form,
    })


@auth_required
def payment(request):
    try:
        order = api_get_order(request.session['order']['id'], request.session['user']['token'])
        user = request.session['user']

        if order and user:
            paypal_dict = paypal_build_params(order, user)

            form = PayPalPaymentsForm(initial=paypal_dict)
            context = {"form": form}
            request.session['order'] = order

            return render(request, "payment.html", context)
    except KeyError:
        return HttpResponseRedirect(reverse('book'))

    return HttpResponseRedirect(reverse('book'))


@auth_required
def summary(request):
    try:
        order = request.session['order']
        del request.session['order']

        return render(request, "summary.html", {'order': order})
    except KeyError:
        return HttpResponseRedirect(reverse('book'))


@auth_required
def calendar(request, year, month):
    """
        Show calendar of events for a given month of a given year.
        ``series_id``
        The event series to show. None shows all event series.

        """
    token = request.session['user']['token']
    orders = api_get_orders(token)
    today = date.today()
    my_year = int(year)
    my_month = int(month)

    if my_month < int(today.month) or my_year < int(today.year):
        my_month = int(today.month)
        my_year = int(today.year)

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
    my_next_year = my_year
    my_next_month = my_month + 1
    if my_next_month == 13:
        my_next_year = my_year + 1
        my_next_month = 1
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
