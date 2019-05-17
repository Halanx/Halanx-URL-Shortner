from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.HomeView.as_view(), name='home'),
    url(r'^(?P<shortcode>[\w-]+)/qrcode\.png', views.qr_code_view, name='qr_code'),
    url(r'^(?P<shortcode>[\w-]+)/', views.redirect_view, name='redirect'),
]
