from django import forms


class OrderForm(forms.Form):
    user = forms.IntegerField(widget=forms.HiddenInput(), required=False)
    address = forms.ChoiceField(label='Adresse')
    vehicle = forms.ChoiceField(label='Vehicule')
    gaz_name = forms.CharField(label='Essence', max_length=255)
    gaz_quantity = forms.FloatField(label='Quantite')
    gaz_price = forms.FloatField(label='Prix au litre')
    date_refill = forms.DateTimeField()
