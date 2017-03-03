from django import forms


class LoginForm(forms.Form):
    email = forms.EmailField(label='Your email')
    password = forms.CharField(label='Your password', widget=forms.PasswordInput())
