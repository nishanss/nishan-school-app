from django.db import models
from academics.models import Grade

class Subject(models.Model):
    name = models.CharField(max_length=100)
    code = models.CharField(max_length=20, unique=True) # e.g., MATH101
    grade = models.ForeignKey(Grade, on_delete=models.CASCADE, related_name='subjects')
    is_elective = models.BooleanField(default=False)
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"{self.name} ({self.grade.name})"

    class Meta:
        ordering = ['grade', 'name']