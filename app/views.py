from django.shortcuts import render
from app.forms import LoginForm
from django.http import HttpResponseRedirect
from component.services.api import login as api_login


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

                return HttpResponseRedirect('/')

            return render(request, 'registration/login.html', {'form': form, 'errors': api_callback['non_field_errors']})

    # if a GET (or any other method) we'll create a blank form
    else:
        form = LoginForm()

    return render(request, 'registration/login.html', {'form': form})
