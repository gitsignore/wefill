from django import forms


class RegisterForm(forms.Form):
    username = forms.CharField(widget=forms.HiddenInput(), required=False)
    firstname = forms.CharField(label='Your firstname', max_length=100)
    lastname = forms.CharField(label='Your lastname', max_length=100)
    email = forms.EmailField(label='Your email')
    password = forms.CharField(label='Your password', widget=forms.PasswordInput())
    confirm_password = forms.CharField(label='Your password', widget=forms.PasswordInput())
