from django import forms


class ProfileForm(forms.Form):
    firstname = forms.CharField(label='Prénom', max_length=100)
    lastname = forms.CharField(label='Nom', max_length=100)
