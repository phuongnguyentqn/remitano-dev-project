from django import forms


class ShareVideoForm(forms.Form):
    url = forms.CharField(max_length=128)
