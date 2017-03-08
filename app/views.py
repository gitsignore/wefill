from calendar import monthrange, calendar
from datetime import date, datetime
from django.shortcuts import render
from app.decorators import auth_required
from app.forms import LoginForm, RegisterForm
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from component.services.api import login as api_login
from component.services.api import register as api_register
from component.services.api import get_user as api_get_user


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
def orders(request):
    return render(request, 'orders.html')


@auth_required
def book(request):
    """
        Show calendar of events for a given month of a given year.
        ``series_id``
        The event series to show. None shows all event series.

        """

    my_year = int(2017)
    my_month = int(3)
    my_calendar_from_month = datetime(my_year, my_month, 1)
    my_calendar_to_month = datetime(my_year, my_month, monthrange(my_year, my_month)[1])

    # Calculate values for the calendar controls. 1-indexed (Jan = 1)
    my_previous_year = my_year
    my_previous_month = my_month - 1
    if my_previous_month == 0:
        my_previous_year = my_year - 1
        my_previous_month = 12
    my_next_year = my_year
    my_next_month = my_month + 1
    if my_next_month == 13:
        my_next_year = my_year + 1
        my_next_month = 1
    my_year_after_this = my_year + 1
    my_year_before_this = my_year - 1
    return render(request, "book.html", {'event_list': '',
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
    return date(1900, month_number, 1).strftime("%B")


def this_month(request):
    """
    Show calendar of events this month.
    """
    today = datetime.now()
    return calendar(request, today.year, today.month)
