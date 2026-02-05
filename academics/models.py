from django.db import models

class AcademicYear(models.Model):
    name = models.CharField(max_length=20)
    is_current = models.BooleanField(default=False)
    
    def __str__(self):
        return self.name

class Grade(models.Model):
    name = models.CharField(max_length=50)

    class Meta:
        ordering = ['name']

    def __str__(self):
        return self.name
    
class Section(models.Model):
    grade = models.ForeignKey(Grade, on_delete=models.CASCADE, related_name='sections')
    name = models.CharField(max_length=10)
    capacity = models.IntegerField(default=30)

    def __str__(self):
        return f"{self.grade.name} - {self.name}"