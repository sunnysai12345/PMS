from django.conf.urls import url
from . import views
from django.conf import settings
from django.conf.urls.static import static


app_name='student'
urlpatterns = [
    #home/ or / or student/
    url(r'login/$', views.StudentLogin.as_view(), name='student_off'),
    url(r'^home/',views.StudentLogin.as_view(), name='student'),
    url(r'^$', views.StudentLogin.as_view(), name='student'),
 #register new student
    url(r'register/$', views.StudentRegistration.as_view(), name='student_register')
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
