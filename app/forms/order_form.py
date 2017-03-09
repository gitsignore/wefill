from django import forms


class OrderForm(forms.Form):
    user = forms.IntegerField(widget=forms.HiddenInput())
    address = forms.IntegerField(label='Adresse')
    vehicle = forms.IntegerField(label='Vehicule')
    gaz_name = forms.CharField(label='Essence', max_length=255)
    gaz_quantity = forms.FloatField(label='Quantite')
    gaz_price = forms.FloatField(label='Prix au litre')
    date_refill = forms.DateTimeField()
