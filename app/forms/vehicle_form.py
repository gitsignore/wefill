from django import forms


class VehicleForm(forms.Form):
    user = forms.IntegerField(widget=forms.HiddenInput(), required=False)
    plate = forms.CharField(label='Plaque d\'immatriculation', max_length=255)
    brand = forms.CharField(label='Marque', max_length=255)
    name = forms.CharField(label='Nom', max_length=255)
    color = forms.CharField(label='Couleur', max_length=255, required=False)
