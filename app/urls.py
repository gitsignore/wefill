from django.conf.urls import url
from django.views.generic import TemplateView
from . import views

urlpatterns = [
    url(r'^$', TemplateView.as_view(template_name='index.html'), name='wefill'),
    url(r'^accounts/login/$', views.login, name='login'),
    url(r'^accounts/register/$', views.register, name='register'),
    url(r'^accounts/logout/$', views.logout, name='logout'),
    url(r'^profile/$', views.profile, name='profile'),
    url(r'^orders/$', views.orders, name='orders'),
    url(r'^book/$', views.book, name='book'),
]
