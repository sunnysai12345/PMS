from django.conf.urls import url
from student import views

app_name='home'
urlpatterns = [
    #home/ or /
    url(r'^$', views.studentlogin, name='home'),
    url(r'^home/',views.studentlogin, name='home'),
]