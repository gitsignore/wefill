import uuid
from django.conf import settings
from paypal.standard.models import ST_PP_COMPLETED
from paypal.standard.ipn.signals import valid_ipn_received


def build_params(order, user):
    """
    Build paypal dict
    :return dict:
    """
    return {
        "business": settings.PAYPAL_API['business'],
        "amount": order['gas_price'],
        "item_name": order['gas_name'],
        "quantity": order['gas_quantity'],
        "currency_code": settings.PAYPAL_API['currency_code'],
        "email": user['email'],
        "first_name": user['firstname'],
        "last_name": user['lastname'],
        "lc": settings.PAYPAL_API['lc'],
        "invoice": str(uuid.uuid4()),
        "notify_url": settings.PAYPAL_API['notify_url'],
        "return_url": settings.PAYPAL_API['return_url'],
        "cancel_return": settings.PAYPAL_API['cancel_return'],
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
        if ipn_obj.receiver_email != settings.PAYPAL_API['business']:
            # Not a valid payment
            return
        # Send PUT to api


valid_ipn_received.connect(save_transaction)
