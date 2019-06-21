from django import forms


class LoginRegisterForm(forms.Form):
    email = forms.EmailField()
    password = forms.CharField(max_length=64)
