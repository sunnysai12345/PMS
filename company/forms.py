from django import forms
from .models import Register
class Postform(forms.ModelForm):
    class Meta:
        model=Register
