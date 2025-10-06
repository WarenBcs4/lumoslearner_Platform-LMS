from django.urls import path
from . import views

urlpatterns = [
    path('checkout/<str:item_type>/<int:item_id>/', views.checkout, name='checkout'),
    path('create/', views.create_payment, name='create_payment'),
    path('success/<uuid:payment_id>/', views.payment_success, name='payment_success'),
    path('cancel/<uuid:payment_id>/', views.payment_cancel, name='payment_cancel'),
    path('history/', views.payment_history, name='payment_history'),
    path('webhook/paypal/', views.paypal_webhook, name='paypal_webhook'),
]