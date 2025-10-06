from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import User, UserProfile


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    list_display = ('username', 'email', 'role', 'is_teacher_approved', 'date_joined')
    list_filter = ('role', 'is_teacher_approved', 'is_staff', 'is_active')
    search_fields = ('username', 'email', 'first_name', 'last_name')
    
    fieldsets = BaseUserAdmin.fieldsets + (
        ('Additional Info', {
            'fields': ('role', 'profile_picture', 'bio', 'phone_number', 
                      'date_of_birth', 'is_teacher_approved')
        }),
    )
    
    actions = ['approve_teachers', 'disapprove_teachers']
    
    def approve_teachers(self, request, queryset):
        queryset.filter(role='teacher').update(is_teacher_approved=True)
        self.message_user(request, f"Approved {queryset.count()} teachers.")
    approve_teachers.short_description = "Approve selected teachers"
    
    def disapprove_teachers(self, request, queryset):
        queryset.filter(role='teacher').update(is_teacher_approved=False)
        self.message_user(request, f"Disapproved {queryset.count()} teachers.")
    disapprove_teachers.short_description = "Disapprove selected teachers"


@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'timezone', 'notifications_enabled')
    search_fields = ('user__username', 'user__email')
    list_filter = ('notifications_enabled', 'email_notifications')