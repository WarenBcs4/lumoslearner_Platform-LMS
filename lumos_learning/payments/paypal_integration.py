import paypalrestsdk
from django.conf import settings
from django.urls import reverse
import logging

logger = logging.getLogger(__name__)

# Configure PayPal SDK
paypalrestsdk.configure({
    "mode": settings.PAYPAL_MODE,
    "client_id": settings.PAYPAL_CLIENT_ID,
    "client_secret": settings.PAYPAL_CLIENT_SECRET
})


def create_paypal_payment(payment_obj, request):
    """Create a PayPal payment"""
    try:
        payment = paypalrestsdk.Payment({
            "intent": "sale",
            "payer": {
                "payment_method": "paypal"
            },
            "redirect_urls": {
                "return_url": request.build_absolute_uri(
                    reverse('payment_success', kwargs={'payment_id': payment_obj.id})
                ),
                "cancel_url": request.build_absolute_uri(
                    reverse('payment_cancel', kwargs={'payment_id': payment_obj.id})
                )
            },
            "transactions": [{
                "item_list": {
                    "items": [{
                        "name": payment_obj.item_name,
                        "sku": str(payment_obj.id),
                        "price": str(payment_obj.amount),
                        "currency": payment_obj.currency,
                        "quantity": 1
                    }]
                },
                "amount": {
                    "total": str(payment_obj.amount),
                    "currency": payment_obj.currency
                },
                "description": f"Payment for {payment_obj.item_name}"
            }]
        })

        if payment.create():
            # Store PayPal payment ID
            payment_obj.paypal_payment_id = payment.id
            payment_obj.save()
            
            # Get approval URL
            for link in payment.links:
                if link.rel == "approval_url":
                    return link.href
        else:
            logger.error(f"PayPal payment creation failed: {payment.error}")
            return None
            
    except Exception as e:
        logger.error(f"PayPal payment creation error: {str(e)}")
        return None


def execute_paypal_payment(payment_id, payer_id):
    """Execute a PayPal payment after user approval"""
    try:
        payment = paypalrestsdk.Payment.find(payment_id)
        
        if payment.execute({"payer_id": payer_id}):
            return True
        else:
            logger.error(f"PayPal payment execution failed: {payment.error}")
            return False
            
    except Exception as e:
        logger.error(f"PayPal payment execution error: {str(e)}")
        return False


def get_paypal_payment_details(payment_id):
    """Get PayPal payment details"""
    try:
        payment = paypalrestsdk.Payment.find(payment_id)
        return payment
    except Exception as e:
        logger.error(f"Error fetching PayPal payment details: {str(e)}")
        return None