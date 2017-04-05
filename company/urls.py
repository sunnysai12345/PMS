from django.conf.urls import url
from . import views
app_name='company'
urlpatterns = [
    url(r'signup', views.post_list, name='signup_page'),
    url(r'login', views.view_home, name='login_page'),
    url(r'edit', views.view_edit, name='home_page'),
    url(r'verify',views.verify,name='verify_page'),
    url(r'users/(?P<username>[A-Za-z_0-9]+)/$', views.profile, name='profile'),
    url(r'jobspecs',views.Jobreqs,name='job_requirements')
]
