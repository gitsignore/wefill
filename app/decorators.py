from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.conf import settings


def auth_required(function):
    def wrap(request, *args, **kwargs):
        if 'is_authenticated' in request.session and request.session['is_authenticated'] is True:
            return function(request, *args, **kwargs)
        else:
            return HttpResponseRedirect(reverse(settings.LOGIN_REDIRECT_URL))

    wrap.__doc__ = function.__doc__
    wrap.__name__ = function.__name__
    return wrap


def admin_required(function):
    def wrap(request, *args, **kwargs):
        if 'is_admin' in request.session and request.session['is_admin'] is True:
            return function(request, *args, **kwargs)
        else:
            return HttpResponseRedirect(reverse(settings.LOGIN_REDIRECT_URL))

    wrap.__doc__ = function.__doc__
    wrap.__name__ = function.__name__
    return wrap
