from django.db import models
from students.models import Student
from academics.models import Section

class Attendance(models.Model):
    STATUS_CHOICES = (
        ('present', 'Present'),
        ('absent', 'Absent'),
        ('leave', 'Leave'),
        ('late', 'Late'),
    )

    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='attendance_records')
    section = models.ForeignKey(Section, on_delete=models.CASCADE)
    date = models.DateField()
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='present')
    remarks = models.TextField(blank=True, null=True)

    class Meta:
        unique_together = ('student', 'date')
        verbose_name_plural = "Attendance"

    def __str__(self):
        return f"{self.student} - {self.date} - {self.status}"