from django import template

register = template.Library()


def is_authenticated(session):
    return 'user' in session and 'is_authenticated' in session


def is_admin(session):
    return 'user' in session and 'is_admin' in session and session['is_admin'] is True


register.filter('is_authenticated', is_authenticated)
register.filter('is_admin', is_admin)
