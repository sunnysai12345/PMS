from django.db import models
from django.core.validators import RegexValidator
from django import forms

# Create your models here.
class Register(models.Model):
    c_name=models.CharField(max_length=20,blank=True,null=True)
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
    #c_file = models.FileField(upload_to="documents/",blank=True)
    def __str__(self):
        return self.c_name

class Edit_Details(models.Model):
    c_perm  = models.ForeignKey(Register, on_delete=models.CASCADE)
    c_name = models.CharField(max_length=20, blank=True, null=True)
    c_email = models.EmailField(blank=True)
    #c_email = models.ForeignKey(Register, on_delete=models.CASCADE)
    c_ctc_offered = models.DecimalField(decimal_places=2,max_digits=8,blank=True)
    c_branches_allowed = models.TextField(blank=True)
    c_requirements = models.TextField(blank=True)
    c_selected_students = models.FileField(upload_to="documents/",blank=True)
    def __str__(self):
        return self.c_name

