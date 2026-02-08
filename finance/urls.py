from django.urls import path
from . import views

urlpatterns = [
    path('', views.invoice_list, name='invoice_list'),
    path('invoices/', views.invoice_list, name='invoice_list'),
    path('create-bulk/', views.invoice_create_bulk, name='invoice_create_bulk'),
    path('<int:pk>/', views.invoice_detail, name='invoice_detail'),
    path('payroll/', views.salary_list, name='salary_list'),
    path('payroll/generate/', views.generate_payroll, name='generate_payroll'),
    path('payroll/pay/<int:pk>/', views.mark_salary_paid, name='mark_salary_paid'),
]