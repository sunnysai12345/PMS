from __future__ import unicode_literals

from django.db import models
#this resolves url
from django.core.urlresolvers import reverse
import datetime
# Create your models here.
class StudentDB(models.Model):
    s_name = models.CharField(max_length=250)
    dob = models.DateField(max_length=12)
    #branch = models.CharField(max_length=50) #search for creating drop down menu
    #course = # search for drop down MTech Btech
    emailid = models.CharField(max_length=250)
    contactno = models.CharField (max_length=20)
    address = models.CharField (max_length=500)
    profile_pic = models.FileField();

    #def get_absolute_url(self):
     #   return reverse('student:student',)

class Course(models.Model):
    course_name=models.CharField(max_length=100)
    shorthand=models.CharField(max_length=5)
