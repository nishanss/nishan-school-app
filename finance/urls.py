from django.urls import path
from . import views

urlpatterns = [
    path('', views.invoice_list, name='invoice_list'),
    path('create-bulk/', views.invoice_create_bulk, name='invoice_create_bulk'),
    path('<int:pk>/', views.invoice_detail, name='invoice_detail'),
]