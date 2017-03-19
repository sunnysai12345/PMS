from django.db import models

# Create your models here.
class Register(models.Model):
    c_name=models.CharField(max_length=20,blank=True,null=True)
    c_details=models.TextField(blank=True)
    c_ad_details=models.TextField(blank=True)
    def __str__(self):
        return self.c_name

