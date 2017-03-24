from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'signup', views.post_list, name='post_list'),
    url(r'login', views.view_home),
    url(r'home', views.view_edit),
    url(r'verify',views.verify),
]
