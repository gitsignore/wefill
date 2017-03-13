import uuid
from django.conf import settings
from django.urls import reverse
from paypal.standard.models import ST_PP_COMPLETED
from paypal.standard.ipn.signals import valid_ipn_received


def build_params():
    """
    Build paypal dict
    :return dict:
    """
    return {
        "business": "maxime.signoret@gmail.com",
        "amount": 1.00,
        "item_name": "Sans Plomb 95",
        "quantity": 20,
        "currency_code": "EUR",
        "address1": "1 rue du test",
        "city": "Paris",
        "zip": "75018",
        "email": "test@test.com",
        "first_name": "test_firstname",
        "last_name": "test_lastname",
        "lc": "FR",
        "invoice": str(uuid.uuid4()),
        "notify_url": "http://127.0.0.1:8000/validate/",
        "return_url": "http://127.0.0.1:8000/order/summary/",
        "cancel_return": "http://127.0.0.1:8000/payment/",
    }


def save_transaction(sender, **kwargs):
    """
    Save transaction on Paypal callback
    :param sender:
    :param kwargs:
    :return:
    """
    ipn_obj = sender
    if ipn_obj.payment_status == ST_PP_COMPLETED:
        # WARNING !
        # Check that the receiver email is the same we previously
        # set on the business field request. (The user could tamper
        # with those fields on payment form before send it to PayPal)
        if ipn_obj.receiver_email != "receiver_email@example.com":
            # Not a valid payment
            return
        # Send PUT to api


valid_ipn_received.connect(save_transaction)
