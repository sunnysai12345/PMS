from django.conf.urls import url
from . import views
app_name='company'
urlpatterns = [
    url(r'signup', views.post_list, name='signup_page'),
    url(r'login', views.view_home, name='login_page'),
    url(r'edit', views.view_edit, name='home_page'),
    url(r'verify',views.verify,name='verify_page'),
    url(r'userc/(?P<username>[A-Za-z_0-9]+)/$', views.profile, name='profile'),
    url(r'jobreqs',views.Jobreqs,name='job_requirements'),
    url(r'change_password', views.change_password,name='passchg'),
    url(r'changed', views.successfull_change,name='passchgsucc'),
    url(r'listjobs',views.listjobs,name='listjobs'),
    url(r'jobs/(?P<jobid>[0-9]+)/',views.jobdesc,name='jobdesc'),
    url(r'applied_msg/', views.jobapplied, name='jobapplied'),
    url(r'student_list/(?P<jobid>[0-9]+)/', views.view_student_list, name='studlist'),
    url(r'taken_name/', views.already_taken, name="takenc"),
    url(r'offered/(?P<userid>[A-Za-z_0-9]+)/$', views.offered, name="takenc"),

]
