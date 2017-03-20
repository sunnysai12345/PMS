from django import forms
from .models import Register
class Postform(forms.ModelForm):
    class Meta:
        model=Register
        fields=['c_name','c_ad_details','c_contact','c_details','c_email']