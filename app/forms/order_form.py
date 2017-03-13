# -*- coding: utf-8 -*-
import datetime

from django import forms


GAS_QUANTITY = (
    ('20', '20 Litres'),
    ('25', '25 Litres'),
    ('30', '30 Litres'),
    ('35', '35 Litres'),
    ('40', '40 Litres'),
    ('45', '45 Litres'),
    ('50', '50 Litres'),
    ('55', '55 Litres'),
    ('60', '60 Litres'),
)


class OrderForm(forms.Form):
    user = forms.IntegerField(widget=forms.HiddenInput(), required=False)
    address = forms.ChoiceField()
    vehicle = forms.ChoiceField()
    gas_name = forms.ChoiceField()
    gas_quantity = forms.ChoiceField(widget=forms.Select, choices=GAS_QUANTITY)
    date_refill = forms.DateTimeField(widget=forms.HiddenInput())

    def __init__(self, data=None, addresses=None, vehicles=None, gas_choices=None, *args, **kwargs):
        super(OrderForm, self).__init__(data, *args, **kwargs)

        if addresses is not None:
            self.fields['address'] = forms.ChoiceField(
                choices=[(str(address['id']), address['name']) for address in addresses]
            )
        if vehicles is not None:
            self.fields['vehicle'] = forms.ChoiceField(
                choices=[(str(vehicle['id']), vehicle['name']) for vehicle in vehicles]
            )
        if gas_choices is not None:
            self.fields['gas_name'] = forms.ChoiceField(
                choices=[(gas['name'], '{0} - {1} €/L'.format(gas['name'], gas['price'])) for gas in gas_choices]
            )
