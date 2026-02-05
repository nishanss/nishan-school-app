from django.urls import path
from . import views

urlpatterns = [
    path('dashboard/', views.academic_dashboard, name='academic_dashboard'),
    path('section/<int:pk>/', views.section_detail, name='section_detail'),
]