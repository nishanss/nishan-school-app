from django.urls import path
from . import views

urlpatterns = [
    path('', views.curriculum_list, name='curriculum_list'),
    path('<int:pk>/', views.curriculum_detail, name='curriculum_detail'),
]