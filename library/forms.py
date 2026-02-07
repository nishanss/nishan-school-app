from django import forms
from .models import Book, BorrowedBook

class BookForm(forms.ModelForm):
    class Meta:
        model = Book
        fields = ['title', 'author', 'isbn', 'category', 'total_copies', 'available_copies']
        widgets = {
            column: forms.TextInput(attrs={'class': 'form-control'}) for column in ['title', 'author', 'isbn', 'category']
        }

class IssueBookForm(forms.ModelForm):
    class Meta:
        model = BorrowedBook
        fields = ['book', 'student', 'issue_date']
        widgets = {
            'book': forms.Select(attrs={'class': 'form-select'}),
            'student': forms.Select(attrs={'class': 'form-select'}),
            'issue_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
        }