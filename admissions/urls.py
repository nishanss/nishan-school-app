from django.urls import path
from . import views

urlpatterns = [
    path('apply/', views.apply_online, name='apply_online'),
    path('dashboard/', views.admission_list, name='admission_list'),
    path('approve/<int:pk>/', views.approve_application, name='approve_application'),
    path('reject/<int:pk>/', views.reject_application, name='reject_application'),
]