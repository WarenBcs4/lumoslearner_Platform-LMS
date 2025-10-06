from django.conf import settings


def site_settings(request):
    return {
        'SITE_NAME': 'Lumos Learning',
        'SITE_DESCRIPTION': 'Comprehensive Learning Management System',
        'PAYPAL_CLIENT_ID': settings.PAYPAL_CLIENT_ID,
        'DEBUG': settings.DEBUG,
    }