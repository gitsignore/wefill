from django.conf.urls import url, include
from django.views.generic import TemplateView
from . import views

urlpatterns = [
    url(r'^$', TemplateView.as_view(template_name='index.html'), name='wefill'),
    url(r'^accounts/login/$', views.login, name='login'),
    url(r'^accounts/register/$', views.register, name='register'),
    url(r'^accounts/logout/$', views.logout, name='logout'),
    url(r'^profile/$', views.profile, name='profile'),
    url(r'^user/address/create/$', views.create_address, name='create_address'),
    url(r'^user/vehicle/create/$', views.create_vehicle, name='create_vehicle'),
    url(r'^user/address/(\d+)/$', views.edit_address, name='edit_address'),
    url(r'^user/address/(\d+)/delete$', views.delete_address, name='delete_address'),
    url(r'^user/vehicle/(\d+)/$', views.edit_vehicle, name='edit_vehicle'),
    url(r'^user/vehicle/(\d+)/delete$', views.delete_vehicle, name='delete_vehicle'),
    url(r'^orders/$', views.orders, name='orders'),
    url(r'^book/$', views.book, name='book'),
    url(r'^calendar/(?P<year>[0-9]{4})/(?P<month>[0-9]{1,2})/$', views.calendar, name='calendar'),
    url(r'^payment/$', views.payment, name='payment'),
    url(r'^order/summary/$', views.summary, name='summary'),
    url(r'^paypal/callback/', include('paypal.standard.ipn.urls')),
]
