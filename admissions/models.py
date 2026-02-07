from django.db import models
from academics.models import Grade

class AdmissionApplication(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending Review'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected'),
    ]

    GENDER_CHOICES = [('M', 'Male'), ('F', 'Female'), ('O', 'Other')]

    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    date_of_birth = models.DateField()
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES)
    
    email = models.EmailField(help_text="Parent's Email Address")
    parent_phone = models.CharField(max_length=15, verbose_name="Parent Phone Number")
    address = models.TextField(blank=True)
    
    grade_applying_for = models.ForeignKey(Grade, on_delete=models.CASCADE, verbose_name="Applying for Grade")
    previous_school = models.CharField(max_length=200, blank=True)
    
    date_applied = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='pending')
    
    notes = models.TextField(blank=True, help_text="Internal staff notes")

    def __str__(self):
        return f"{self.first_name} {self.last_name} - {self.grade_applying_for}"