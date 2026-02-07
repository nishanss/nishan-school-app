from django.db import models
from django.utils import timezone
from students.models import Student
from datetime import timedelta

class Book(models.Model):
    title = models.CharField(max_length=200)
    author = models.CharField(max_length=200)
    isbn = models.CharField(max_length=20, unique=True, verbose_name="ISBN")
    category = models.CharField(max_length=100, blank=True)
    total_copies = models.PositiveIntegerField(default=1)
    available_copies = models.PositiveIntegerField(default=1)

    def __str__(self):
        return f"{self.title} by {self.author}"

class BorrowedBook(models.Model):
    STATUS_CHOICES = [
        ('issued', 'Issued'),
        ('returned', 'Returned'),
    ]

    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    issue_date = models.DateField(default=timezone.now)
    due_date = models.DateField(blank=True)
    return_date = models.DateField(null=True, blank=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='issued')

    def save(self, *args, **kwargs):
        if not self.due_date:
            self.due_date = self.issue_date + timedelta(days=14)
        
        if not self.pk:
            self.book.available_copies -= 1
            self.book.save()
        super().save(*args, **kwargs)

    def mark_as_returned(self):
        if self.status != 'returned':
            self.status = 'returned'
            self.return_date = timezone.now().date()
            self.book.available_copies += 1
            self.book.save()
            self.save()

    def __str__(self):
        return f"{self.book.title} - {self.student.first_name}"