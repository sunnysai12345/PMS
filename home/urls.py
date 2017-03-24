from django.conf.urls import url
from . import views

app_name='home'
urlpatterns = [
    #home/ or /
    url(r'^$', views.home, name='home'),
    url(r'^home/',views.home, name='home'),
]