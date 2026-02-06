from django.urls import path
from . import views

urlpatterns = [
    path('', views.exam_list, name='exam_list'),
    
    path('enter-marks/<int:exam_id>/', views.enter_marks, name='enter_marks'),
]