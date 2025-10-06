from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView, DetailView
from django.contrib import messages
from django.http import JsonResponse, HttpResponse
from django.core.paginator import Paginator
from .models import Course, Category, Material, Enrollment, Progress, Review
from payments.models import Payment


class CourseListView(ListView):
    model = Course
    template_name = 'courses/course_list.html'
    context_object_name = 'courses'
    paginate_by = 12
    
    def get_queryset(self):
        queryset = Course.objects.filter(is_published=True)
        category = self.request.GET.get('category')
        difficulty = self.request.GET.get('difficulty')
        search = self.request.GET.get('search')
        
        if category:
            queryset = queryset.filter(category__slug=category)
        if difficulty:
            queryset = queryset.filter(difficulty=difficulty)
        if search:
            queryset = queryset.filter(title__icontains=search)
            
        return queryset.order_by('-created_at')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = Category.objects.all()
        context['selected_category'] = self.request.GET.get('category', '')
        context['selected_difficulty'] = self.request.GET.get('difficulty', '')
        context['search_query'] = self.request.GET.get('search', '')
        return context


class CourseDetailView(DetailView):
    model = Course
    template_name = 'courses/course_detail.html'
    context_object_name = 'course'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        course = self.get_object()
        
        context['materials'] = course.materials.all().order_by('order')
        context['reviews'] = course.reviews.filter(is_approved=True).order_by('-created_at')[:5]
        context['is_enrolled'] = False
        context['enrollment'] = None
        
        if self.request.user.is_authenticated:
            try:
                enrollment = Enrollment.objects.get(student=self.request.user, course=course)
                context['is_enrolled'] = True
                context['enrollment'] = enrollment
            except Enrollment.DoesNotExist:
                pass
                
        return context


@login_required
def enroll_course(request, slug):
    course = get_object_or_404(Course, slug=slug, is_published=True)
    
    enrollment, created = Enrollment.objects.get_or_create(
        student=request.user,
        course=course,
        defaults={'is_active': True}
    )
    
    if created:
        messages.success(request, f'Successfully enrolled in {course.title}!')
    else:
        messages.info(request, f'You are already enrolled in {course.title}.')
    
    return redirect('course_detail', slug=slug)


@login_required
def pdf_viewer(request, material_id):
    material = get_object_or_404(Material, id=material_id, material_type='pdf')
    
    # Check if user has access
    enrollment = get_object_or_404(Enrollment, student=request.user, course=material.course)
    
    # Check if material is free or user has paid
    has_access = material.is_free
    if not has_access:
        payment = Payment.objects.filter(
            user=request.user,
            material=material,
            status='completed'
        ).exists()
        has_access = payment
    
    context = {
        'material': material,
        'has_access': has_access,
        'free_pages': 10 if not has_access else None
    }
    
    return render(request, 'courses/pdf_viewer.html', context)


@login_required
def video_player(request, material_id):
    material = get_object_or_404(Material, id=material_id, material_type='video')
    
    # Check if user has access
    enrollment = get_object_or_404(Enrollment, student=request.user, course=material.course)
    
    # Check if material is free or user has paid
    has_access = material.is_free
    if not has_access:
        payment = Payment.objects.filter(
            user=request.user,
            material=material,
            status='completed'
        ).exists()
        has_access = payment
    
    # For videos, first episode is always free
    is_first_episode = material.order == 1
    if is_first_episode:
        has_access = True
    
    context = {
        'material': material,
        'has_access': has_access,
        'is_first_episode': is_first_episode
    }
    
    return render(request, 'courses/video_player.html', context)


@login_required
def mark_progress(request, material_id):
    if request.method == 'POST':
        material = get_object_or_404(Material, id=material_id)
        enrollment = get_object_or_404(Enrollment, student=request.user, course=material.course)
        
        progress, created = Progress.objects.get_or_create(
            enrollment=enrollment,
            material=material,
            defaults={'is_completed': True}
        )
        
        if not created:
            progress.is_completed = True
            progress.save()
        
        # Update enrollment progress
        total_materials = material.course.materials.count()
        completed_materials = Progress.objects.filter(
            enrollment=enrollment,
            is_completed=True
        ).count()
        
        enrollment.progress_percentage = int((completed_materials / total_materials) * 100)
        enrollment.save()
        
        return JsonResponse({'success': True, 'progress': enrollment.progress_percentage})
    
    return JsonResponse({'success': False})


@login_required
def submit_review(request, slug):
    if request.method == 'POST':
        course = get_object_or_404(Course, slug=slug)
        
        # Check if user is enrolled
        enrollment = get_object_or_404(Enrollment, student=request.user, course=course)
        
        rating = int(request.POST.get('rating', 0))
        comment = request.POST.get('comment', '')
        
        if 1 <= rating <= 5:
            review, created = Review.objects.get_or_create(
                course=course,
                student=request.user,
                defaults={
                    'rating': rating,
                    'comment': comment,
                    'is_approved': False
                }
            )
            
            if created:
                messages.success(request, 'Review submitted successfully! It will be visible after approval.')
            else:
                review.rating = rating
                review.comment = comment
                review.is_approved = False
                review.save()
                messages.success(request, 'Review updated successfully!')
        else:
            messages.error(request, 'Invalid rating. Please select 1-5 stars.')
    
    return redirect('course_detail', slug=slug)