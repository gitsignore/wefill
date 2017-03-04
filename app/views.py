from django.shortcuts import render

from app.decorators import auth_required
from app.forms import LoginForm, RegisterForm
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from component.services.api import login as api_login
from component.services.api import register as api_register


def login(request):
    # if this is a POST request we need to process the form data
    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        form = LoginForm(request.POST)
        # check whether it's valid:
        if form.is_valid():
            api_callback = api_login(form.cleaned_data['email'], form.cleaned_data['password'])
            if 'token' in api_callback:
                request.session['token'] = api_callback['token']
                request.session['is_authenticated'] = True
                if 'is_admin' in api_callback:
                    request.session['is_admin'] = api_callback['is_admin']

                return HttpResponseRedirect(reverse('wefill'))

            return render(request, 'registration/login.html', {'form': form, 'errors': api_callback['non_field_errors']})

    # if a GET (or any other method) we'll create a blank form
    else:
        form = LoginForm()

    return render(request, 'registration/login.html', {'form': form})


def register(request):
    # if this is a POST request we need to process the form data
    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        form = RegisterForm(request.POST)
        # check whether it's valid:
        if form.is_valid():
            form.cleaned_data['username'] = form.cleaned_data['email']
            api_callback = api_register(form.cleaned_data)
            if 'token' in api_callback:
                request.session['token'] = api_callback['token']
                request.session['is_authenticated'] = True
                if 'is_admin' in api_callback:
                    request.session['is_admin'] = api_callback['is_admin']

                return HttpResponseRedirect(reverse('wefill'))
            return render(request, 'registration/register.html', {
                'form': form, 'errors': api_callback['errors']
            })

    # if a GET (or any other method) we'll create a blank form
    else:
        form = RegisterForm()

    return render(request, 'registration/register.html', {'form': form})


def logout(request):
    try:
        del request.session['token']
        del request.session['is_authenticated']
        del request.session['is_admin']
    except KeyError:
        pass
    return HttpResponseRedirect(reverse('wefill'))


@auth_required
def test(request):
    return render(request, 'test.html')
