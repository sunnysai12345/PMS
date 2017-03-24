from django import forms
from .models import Register,Edit_Details
from django.contrib.auth.forms import AuthenticationForm
class Postform(forms.ModelForm):
    class Meta:
        model=Register
        widgets = {
            'c_password': forms.PasswordInput(),
            'c_confirm_password' : forms.PasswordInput(),
        }
        fields=['c_name','c_contact','c_details','c_email','c_password']
class Loginform(AuthenticationForm):
    username = forms.CharField(label="Username", max_length=30,
                               widget=forms.TextInput(attrs={'class': 'form-control', 'name': 'username'}))
    password = forms.CharField(label="Password", max_length=30,
                               widget=forms.TextInput(attrs={'class': 'form-control', 'name': 'password'}))
    def clean(self):
        pass
class EditForm(forms.ModelForm):
    class Meta :
        model = Edit_Details
        fields=['c_name','c_email','c_branches_allowed','c_ctc_offered','c_requirements','c_selected_students']
