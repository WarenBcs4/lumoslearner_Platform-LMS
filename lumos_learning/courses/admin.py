from django.contrib import admin
from .models import Category, Course, Material, Enrollment, Progress, Review, Certificate


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug', 'created_at')
    prepopulated_fields = {'slug': ('name',)}
    search_fields = ('name',)


class MaterialInline(admin.TabularInline):
    model = Material
    extra = 1
    fields = ('title', 'material_type', 'file', 'is_free', 'price', 'order')


@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ('title', 'instructor', 'category', 'price', 'is_published', 'created_at')
    list_filter = ('category', 'difficulty', 'is_published', 'is_featured')
    search_fields = ('title', 'instructor__username')
    prepopulated_fields = {'slug': ('title',)}
    inlines = [MaterialInline]
    
    actions = ['publish_courses', 'unpublish_courses']
    
    def publish_courses(self, request, queryset):
        queryset.update(is_published=True)
        self.message_user(request, f"Published {queryset.count()} courses.")
    publish_courses.short_description = "Publish selected courses"
    
    def unpublish_courses(self, request, queryset):
        queryset.update(is_published=False)
        self.message_user(request, f"Unpublished {queryset.count()} courses.")
    unpublish_courses.short_description = "Unpublish selected courses"


@admin.register(Material)
class MaterialAdmin(admin.ModelAdmin):
    list_display = ('title', 'course', 'material_type', 'is_free', 'price', 'order')
    list_filter = ('material_type', 'is_free')
    search_fields = ('title', 'course__title')


@admin.register(Enrollment)
class EnrollmentAdmin(admin.ModelAdmin):
    list_display = ('student', 'course', 'enrolled_at', 'progress_percentage', 'is_active')
    list_filter = ('is_active', 'enrolled_at')
    search_fields = ('student__username', 'course__title')


@admin.register(Progress)
class ProgressAdmin(admin.ModelAdmin):
    list_display = ('enrollment', 'material', 'is_completed', 'completed_at')
    list_filter = ('is_completed',)
    search_fields = ('enrollment__student__username', 'material__title')


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ('course', 'student', 'rating', 'is_approved', 'created_at')
    list_filter = ('rating', 'is_approved')
    search_fields = ('course__title', 'student__username')
    
    actions = ['approve_reviews', 'disapprove_reviews']
    
    def approve_reviews(self, request, queryset):
        queryset.update(is_approved=True)
        self.message_user(request, f"Approved {queryset.count()} reviews.")
    approve_reviews.short_description = "Approve selected reviews"
    
    def disapprove_reviews(self, request, queryset):
        queryset.update(is_approved=False)
        self.message_user(request, f"Disapproved {queryset.count()} reviews.")
    disapprove_reviews.short_description = "Disapprove selected reviews"


@admin.register(Certificate)
class CertificateAdmin(admin.ModelAdmin):
    list_display = ('enrollment', 'certificate_id', 'issued_at', 'is_valid')
    list_filter = ('is_valid', 'issued_at')
    search_fields = ('enrollment__student__username', 'certificate_id')