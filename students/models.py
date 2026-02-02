from django.db import models

class Student(models.Model):
    GENDER_CHOICES = [
        ('M', 'Male'),
        ('F', 'Female'),
        ('O', 'Other'),
    ]

    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    roll_number = models.CharField(max_length=20, unique=True)
    date_of_birth = models.DateField()
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES)

    email = models.EmailField(unique=True)
    parent_phone = models.CharField(max_length=10)
    
    admission_date = models.DateField(auto_now_add=True)
    is_active = models.BooleanField(default=True)
    photo = models.ImageField(upload_to='students/', null=True, blank=True)

    def __str__(self):
        return f"{self.first_name} {self.last_name} ({self.roll_number})"