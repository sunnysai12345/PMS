from django.db import models

# Create your models here.
class Register(models.Model):
    c_name=models.TextField(null=True)
    def __str__(self):
        return 3

