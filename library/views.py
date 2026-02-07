from django.shortcuts import render, redirect, get_object_or_404
from .models import Book, BorrowedBook
from .forms import BookForm, IssueBookForm
from django.utils import timezone

def book_list(request):
    books = Book.objects.all()
    return render(request, 'library/book_list.html', {'books': books})

def add_book(request):
    form = BookForm(request.POST or None)
    if form.is_valid():
        form.save()
        return redirect('book_list')
    return render(request, 'library/book_form.html', {'form': form, 'title': 'Add New Book'})

def issue_book(request):
    form = IssueBookForm(request.POST or None)
    if form.is_valid():
        form.save()
        return redirect('issued_books')
    return render(request, 'library/book_form.html', {'form': form, 'title': 'Issue a Book'})

def return_book(request, pk):
    issue = get_object_or_404(BorrowedBook, pk=pk)
    if issue.status != 'returned':
        issue.status = 'returned'
        issue.return_date = timezone.now().date()
        issue.book.available_copies += 1
        issue.book.save()
        issue.save()
    return redirect('issued_books')

def issued_books(request):
    current_status = request.GET.get('status')
    query_set = BorrowedBook.objects.all().select_related('book', 'student__section__grade').order_by('-issue_date')
    # issued = BorrowedBook.objects.filter(status='issued').select_related('book', 'student__section__grade')


    if current_status:
        query_set = query_set.filter(status=current_status)

    # if current_status:
    #     issued = issued.filter(status=current_status)

    return render(request, 'library/issued_books.html', {
        'issued': query_set, 
        'today': timezone.now().date(),
        'current_status': current_status,
        'status_choices': BorrowedBook.STATUS_CHOICES,
    })