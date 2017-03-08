from django import forms


class AddressForm(forms.Form):
    user = forms.IntegerField(widget=forms.HiddenInput())
    name = forms.CharField(label='Nom', max_length=255)
    street = forms.CharField(label='Rue', max_length=255)
    city = forms.CharField(label='Ville', max_length=255)
    zip = forms.CharField(label='Code postal', max_length=10)
