from django import forms


class VehicleForm(forms.Form):
    user = forms.IntegerField(widget=forms.HiddenInput())
    plate = forms.CharField(label='Plaque d\'immatriculation', max_length=255, blank=False)
    brand = forms.CharField(label='Marque', max_length=255, blank=False)
    name = forms.CharField(label='Nom', max_length=255, blank=False)
    color = forms.CharField(label='Couleur', max_length=255, blank=True)
