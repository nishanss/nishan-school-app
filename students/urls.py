from django.contrib import admin
from django.urls import include, path
from . import views

urlpatterns = [
    path("", views.student_list, name='student_list'),
    path("create/", views.student_create, name='student_create'),
    path("<int:pk>/", views.student_detail, name='student_detail'),
    path("<int:pk>/update/", views.student_update, name='student_update'),
    path('<int:pk>/report/', views.download_report_card, name='download_report_card'),
    path("excel/", views.export_students_excel, name='export_students_excel'),
]