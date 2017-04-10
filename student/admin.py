from django.contrib import admin

# Register your models here.
from .models import StudentDB,Notifications,AppliedJob
# Register your models here.
admin.site.register(StudentDB)
admin.site.register(Notifications)
admin.site.register(AppliedJob)
