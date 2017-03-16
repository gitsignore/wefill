from django import forms


class GasForm(forms.Form):
    name = forms.CharField(label='Nom', max_length=255)
    price = forms.FloatField(label='Prix')
