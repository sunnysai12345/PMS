from __future__ import unicode_literals

from django.db import models
#this resolves url
from django.core.urlresolvers import reverse
import datetime
from company.models import Job_desc
# Create your models here.
class StudentDB(models.Model):
    BRANCH=(
        ('BTECH','bachelors'),
        ('MTECH','masters'),
        ('PHD','philospher'),
    )
    COURSE=(
        ('CS','computer_science'),
        ('ME','mechanical'),
        ('EE','electrical'),
    )
    s_username = models.CharField(max_length=250, default='')
    s_name = models.CharField(max_length=250,blank=True)
    s_password = models.CharField(max_length=250, blank=True)
    s_confirm_password=models.CharField(max_length=250, blank=True)
    dob = models.DateField()
    emailid = models.EmailField(blank=True)
    branch = models.CharField(max_length=10,choices=BRANCH, default='CS') #search for creating drop down menu
    course =  models.CharField(max_length=5,choices=COURSE, default='BTECH')#search for drop down MTech Btech
    s_verified = models.BooleanField(default=False, blank=True)
    s_verification = models.IntegerField(default=0, blank=True)
    contactno = models.CharField (max_length=20,blank=True)
    #address = models.CharField (max_length=500)
    #profile_pic = models.FileField();

    #def get_absolute_url(self):
     #   return reverse('student:student',)

class Edit_Details(models.Model):
    #s_perm  = models.ForeignKey(StudentDB, on_delete=models.CASCADE)
    s_name = models.CharField(max_length=250, blank=True, null=True)
    emailid = models.EmailField(blank=True)
    qualification=models.CharField(max_length=250,blank=True, null=True)
    resume=models.FileField(upload_to="documents/",blank=True)
    def __str__(self):
        return self.s_name

class Notifications(models.Model):
    job_id = models.ForeignKey(Job_desc, on_delete=models.CASCADE)
    n_text=models.CharField(max_length=250)
    new=models.BooleanField()

class AppliedJob(models.Model):
    job_id= models.ForeignKey(Job_desc, on_delete=models.CASCADE)
    applied=models.BooleanField()
'''
class Course(models.Model):
    course_name=models.CharField(max_length=100)
    shorthand=models.CharField(max_length=5)
'''