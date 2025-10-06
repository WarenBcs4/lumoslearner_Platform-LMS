from django.urls import path
from . import views

urlpatterns = [
    path('', views.CourseListView.as_view(), name='course_list'),
    path('<slug:slug>/', views.CourseDetailView.as_view(), name='course_detail'),
    path('<slug:slug>/enroll/', views.enroll_course, name='enroll_course'),
    path('<slug:slug>/review/', views.submit_review, name='submit_review'),
    path('material/<int:material_id>/pdf/', views.pdf_viewer, name='pdf_viewer'),
    path('material/<int:material_id>/video/', views.video_player, name='video_player'),
    path('material/<int:material_id>/progress/', views.mark_progress, name='mark_progress'),
]