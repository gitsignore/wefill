from django import template

register = template.Library()


def is_authenticated(session):
    if 'user' in session and 'is_authenticated' in session:
        return True
    return False


def is_admin(session):
    if 'user' in session and 'is_admin' in session:
        return True
    return False


register.filter('is_authenticated', is_authenticated)
register.filter('is_admin', is_admin)
