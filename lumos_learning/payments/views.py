from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from django.views.generic import TemplateView
from django.conf import settings
from courses.models import Course, Material
from .models import Payment, PaymentHistory
from .paypal_integration import create_paypal_payment, execute_paypal_payment
import json


@login_required
def checkout(request, item_type, item_id):
    """Checkout page for course or material"""
    if item_type == 'course':
        item = get_object_or_404(Course, id=item_id)
        amount = item.price
    elif item_type == 'material':
        item = get_object_or_404(Material, id=item_id)
        amount = item.price
    else:
        messages.error(request, 'Invalid item type.')
        return redirect('course_list')
    
    if amount <= 0:
        messages.error(request, 'This item is free.')
        return redirect('course_list')
    
    context = {
        'item': item,
        'item_type': item_type,
        'amount': amount,
        'paypal_client_id': settings.PAYPAL_CLIENT_ID,
    }
    
    return render(request, 'payments/checkout.html', context)


@login_required
def create_payment(request):
    """Create a payment record and initiate payment process"""
    if request.method == 'POST':
        item_type = request.POST.get('item_type')
        item_id = request.POST.get('item_id')
        payment_method = request.POST.get('payment_method')
        
        # Get the item
        if item_type == 'course':
            course = get_object_or_404(Course, id=item_id)
            material = None
            amount = course.price
        elif item_type == 'material':
            material = get_object_or_404(Material, id=item_id)
            course = None
            amount = material.price
        else:
            return JsonResponse({'success': False, 'error': 'Invalid item type'})
        
        # Create payment record
        payment = Payment.objects.create(
            user=request.user,
            course=course,
            material=material,
            amount=amount,
            payment_method=payment_method,
            status='pending'
        )
        
        # Create payment history entry
        PaymentHistory.objects.create(
            payment=payment,
            status='pending',
            notes='Payment initiated'
        )
        
        if payment_method == 'paypal':
            approval_url = create_paypal_payment(payment, request)
            if approval_url:
                return JsonResponse({
                    'success': True,
                    'approval_url': approval_url,
                    'payment_id': str(payment.id)
                })
            else:
                payment.status = 'failed'
                payment.save()
                PaymentHistory.objects.create(
                    payment=payment,
                    status='failed',
                    notes='PayPal payment creation failed'
                )
                return JsonResponse({'success': False, 'error': 'Payment creation failed'})
        
        elif payment_method == 'intersend':
            # TODO: Implement InterSend integration
            return JsonResponse({'success': False, 'error': 'InterSend not implemented yet'})
        
        else:
            return JsonResponse({'success': False, 'error': 'Invalid payment method'})
    
    return JsonResponse({'success': False, 'error': 'Invalid request method'})


@login_required
def payment_success(request, payment_id):
    """Handle successful payment return from PayPal"""
    payment = get_object_or_404(Payment, id=payment_id, user=request.user)
    
    payer_id = request.GET.get('PayerID')
    if payer_id and payment.paypal_payment_id:
        if execute_paypal_payment(payment.paypal_payment_id, payer_id):
            payment.status = 'completed'
            payment.save()
            
            PaymentHistory.objects.create(
                payment=payment,
                status='completed',
                notes='Payment completed successfully'
            )
            
            messages.success(request, 'Payment completed successfully!')
            
            # Redirect to appropriate content
            if payment.course:
                return redirect('course_detail', slug=payment.course.slug)
            elif payment.material:
                if payment.material.material_type == 'pdf':
                    return redirect('pdf_viewer', material_id=payment.material.id)
                elif payment.material.material_type == 'video':
                    return redirect('video_player', material_id=payment.material.id)
        else:
            payment.status = 'failed'
            payment.save()
            
            PaymentHistory.objects.create(
                payment=payment,
                status='failed',
                notes='PayPal payment execution failed'
            )
            
            messages.error(request, 'Payment execution failed.')
    
    return render(request, 'payments/payment_success.html', {'payment': payment})


@login_required
def payment_cancel(request, payment_id):
    """Handle cancelled payment"""
    payment = get_object_or_404(Payment, id=payment_id, user=request.user)
    
    payment.status = 'failed'
    payment.save()
    
    PaymentHistory.objects.create(
        payment=payment,
        status='failed',
        notes='Payment cancelled by user'
    )
    
    messages.warning(request, 'Payment was cancelled.')
    return render(request, 'payments/payment_cancel.html', {'payment': payment})


@login_required
def payment_history(request):
    """Display user's payment history"""
    payments = Payment.objects.filter(user=request.user).order_by('-created_at')
    
    context = {
        'payments': payments
    }
    
    return render(request, 'payments/payment_history.html', context)


@csrf_exempt
def paypal_webhook(request):
    """Handle PayPal webhook notifications"""
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            event_type = data.get('event_type')
            
            if event_type == 'PAYMENT.SALE.COMPLETED':
                # Handle completed payment
                pass
            elif event_type == 'PAYMENT.SALE.DENIED':
                # Handle denied payment
                pass
            
            return JsonResponse({'status': 'success'})
        except Exception as e:
            return JsonResponse({'status': 'error', 'message': str(e)})
    
    return JsonResponse({'status': 'error', 'message': 'Invalid request method'})