from django import template

register = template.Library()


def is_authenticated(session):
    if 'user' in session and 'is_authenticated' in session:
        return True
    return False


register.filter('is_authenticated', is_authenticated)
