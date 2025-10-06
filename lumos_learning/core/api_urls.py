from django.urls import path, include
from rest_framework.routers import DefaultRouter

router = DefaultRouter()

urlpatterns = [
    path('', include(router.urls)),
    path('courses/', include('courses.api_urls')),
    path('payments/', include('payments.api_urls')),
]