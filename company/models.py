from django.db import models
from django.core.validators import RegexValidator

# Create your models here.
class Register(models.Model):
    c_name=models.CharField(max_length=20,blank=True,null=True)
    c_details=models.TextField(blank=True)
    c_ad_details=models.TextField(blank=True)
    phone_regex = RegexValidator(regex=r'^\+?1?\d{9,15}$',
                                 message="Phone number must be entered in the format: '+999999999'. Up to 15 digits allowed.")
    c_contact = models.CharField(validators=[phone_regex], blank=True,max_length=15)  # validators should be a list
    c_email = models.EmailField(blank=True)
    def __str__(self):
        return self.c_name

