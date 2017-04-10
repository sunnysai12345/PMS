from django.db import models
from django.core.validators import RegexValidator
from django import forms

# Create your models here.
class Register(models.Model):
    c_name=models.CharField(max_length=20,blank=True,null=True,unique=True)
    c_company_name=models.CharField(max_length=20,blank=True,null=True)
    c_details=models.TextField(blank=True)
    c_verified=models.BooleanField(default=False,blank=True)
    c_verification=models.IntegerField(default=0,blank=True)
    #c_ad_details=models.TextField(blank=True)
    phone_regex = RegexValidator(regex=r'^\+?1?\d{9,15}$',
                                 message="Phone number must be entered in the format: '+999999999'. Up to 15 digits allowed.")
    c_contact = models.CharField(validators=[phone_regex], blank=True,max_length=15)  # validators should be a list
    c_email = models.EmailField(blank=True)
    c_password=models.CharField(max_length=30,blank=True)
    c_confirm_password=models.CharField(max_length=30,blank=True)
    c_ppt = models.FileField(upload_to="documents/", blank=True)
    #c_file = models.FileField(upload_to="documents/",blank=True)
    def __str__(self):
        return str(self.c_name)

class Edit_Details(models.Model):
    register  = models.ForeignKey(Register, on_delete=models.CASCADE)
    c_email = models.EmailField(blank=True)
    #c_email = models.ForeignKey(Register, on_delete=models.CASCADE)
    c_ppt = models.FileField(upload_to="documents/",blank=True)
    def __str__(self):
        return str(self.c_name)
class Job_desc(models.Model):
    COURSE = (
        ('BTECH', 'bachelors'),
        ('MTECH', 'masters'),
        ('PHD', 'philospher'),
    )
    BRANCH = (
        ('CS', 'computer_science'),
        ('ME', 'mechanical'),
        ('EE', 'electrical'),
    )
    register = models.ForeignKey('Register', on_delete=models.CASCADE,null=True)
    c_position = models.CharField(max_length=30,blank=True,null=True)
    list_of_student=models.CharField(max_length=500,blank=True,null=True)
    #selected_students=models.CharField(max_length=500,blank=True,null=True)
    c_description=models.CharField(max_length=500,null=True)
    date_published = models.DateField(null=True)
    date_expiry=models.DateField(null=True)
    c_ctc_offered = models.DecimalField(decimal_places=2, max_digits=8, blank=True,null=True)
    c_branch = models.CharField(max_length=10, choices=BRANCH, default='CS')  # search for creating drop down menu
    c_course = models.CharField(max_length=5, choices=COURSE, default='BTECH')  # search for drop down MTech Btech
    def __str__(self):
        return str(self.c_position)
