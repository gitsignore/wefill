from django.conf.urls import url
from django.views.generic import TemplateView
from . import views

urlpatterns = [
    url(r'^$', TemplateView.as_view(template_name='index.html'), name='wefill'),
    url(r'^account/login/$', views.login, name='login'),
    url(r'^account/register/$', views.register, name='register'),
    url(r'^account/logout/$', views.logout, name='logout'),
]
