# -*- coding: utf-8 -*-
from django import forms


class RegisterForm(forms.Form):
    username = forms.CharField(widget=forms.HiddenInput(), required=False)
    firstname = forms.CharField(label='Prénom', max_length=100)
    lastname = forms.CharField(label='Nom', max_length=100)
    email = forms.EmailField(label='Email')
    password = forms.CharField(label='Mot de passe', widget=forms.PasswordInput())
    confirm_password = forms.CharField(label='Confirmation du mot de passe', widget=forms.PasswordInput())
