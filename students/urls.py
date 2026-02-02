from django.contrib import admin
from django.urls import include, path
from . import views

urlpatterns = [
    path("", views.student_list, name='student_list'),
]