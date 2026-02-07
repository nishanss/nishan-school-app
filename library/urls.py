from django.urls import path
from . import views

urlpatterns = [
    path('', views.book_list, name='book_list'),
    path('add/', views.add_book, name='add_book'),
    path('issue/', views.issue_book, name='issue_book'),
    path('return/<int:pk>/', views.return_book, name='return_book'),
    path('issued/', views.issued_books, name='issued_books'),
]