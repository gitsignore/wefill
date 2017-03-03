from django.conf.urls import url
from django.contrib.auth import views as auth_views
from django.views.generic import TemplateView
from . import views

urlpatterns = [
    url(r'^$', TemplateView.as_view(template_name='index.html'), name='wifill'),
    url(r'^account/login/$', views.login, name='login'),
    url(r'^account/logout/$', auth_views.logout, {'next_page': '/'}, name='logout'),
]
