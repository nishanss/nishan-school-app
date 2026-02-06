from django.db import models
from django.contrib.auth.models import User

class Staff(models.Model):
    ROLE_CHOICES = [
        ('ADMIN', 'Administrator'),
        ('TEACHER', 'Teacher'),
        ('ACCOUNTANT', 'Accountant'),
        ('LIBRARIAN', 'Librarian'),
        ('TRANSPORT', 'Transport Manager'),
        ('OTHER', 'Other Support Staff'),
    ]

    GENDER_CHOICES = [('M', 'Male'), ('F', 'Female'), ('O', 'Other')]

    user = models.OneToOneField(User, on_delete=models.SET_NULL, null=True, blank=True)
    staff_id = models.CharField(max_length=20, unique=True)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='TEACHER')
    
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=20)
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES)
    date_of_birth = models.DateField()
    joining_date = models.DateField()
    
    is_active = models.BooleanField(default=True)
    qualification = models.CharField(max_length=100, help_text="e.g. B.Ed, M.Sc")
    experience_years = models.PositiveIntegerField(default=0)
    address = models.TextField()
    
    base_salary = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)

    class Meta:
        verbose_name_plural = "Staff Members"

    def __str__(self):
        return f"{self.first_name} {self.last_name} ({self.role})"