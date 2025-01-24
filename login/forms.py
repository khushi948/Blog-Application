from django import forms

class UserRegister(forms.Form):
    name = forms.CharField(label='Name', max_length=100)
    email = forms.EmailField(label='Email')
    phone_no = forms.CharField(label='PhoneNo.')
    password = forms.CharField(label='password', max_length=100)
    retype_password = forms.CharField(label='Retype Password', max_length=100)