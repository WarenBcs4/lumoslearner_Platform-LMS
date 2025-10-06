from django.shortcuts import render, redirect
from django.views.generic import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db import models
from courses.models import Course, Enrollment
from payments.models import Payment


class HomeView(TemplateView):
    template_name = 'home.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['featured_courses'] = Course.objects.filter(is_published=True)[:6]
        context['total_courses'] = Course.objects.filter(is_published=True).count()
        context['total_students'] = Enrollment.objects.values('student').distinct().count()
        return context


class DashboardView(LoginRequiredMixin, TemplateView):
    template_name = 'dashboard.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user
        
        if user.role == 'student':
            context['enrolled_courses'] = Enrollment.objects.filter(
                student=user, is_active=True
            ).select_related('course')
            context['recent_payments'] = Payment.objects.filter(
                user=user
            ).order_by('-created_at')[:5]
            
        elif user.role == 'teacher':
            context['my_courses'] = Course.objects.filter(instructor=user)
            context['total_students'] = Enrollment.objects.filter(
                course__instructor=user
            ).count()
            context['total_revenue'] = Payment.objects.filter(
                course__instructor=user, status='completed'
            ).aggregate(total=models.Sum('amount'))['total'] or 0
            
        return context


@login_required
def profile_view(request):
    if request.method == 'POST':
        # Handle profile updates
        user = request.user
        user.first_name = request.POST.get('first_name', '')
        user.last_name = request.POST.get('last_name', '')
        user.bio = request.POST.get('bio', '')
        user.phone_number = request.POST.get('phone_number', '')
        user.save()
        
        messages.success(request, 'Profile updated successfully!')
        return redirect('profile')
    
    return render(request, 'profile.html')