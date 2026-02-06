from django.db import models
from academics.models import Grade
from subjects.models import Subject

class Curriculum(models.Model):
    grade = models.ForeignKey(Grade, on_delete=models.CASCADE)
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE)
    academic_year = models.CharField(max_length=20, default="2025-2026")

    class Meta:
        unique_together = ('grade', 'subject', 'academic_year')

    def __str__(self):
        return f"{self.subject.name} for {self.grade.name}"

class LessonPlan(models.Model):
    curriculum = models.ForeignKey(Curriculum, on_delete=models.CASCADE, related_name='lessons')
    title = models.CharField(max_length=200) # e.g., "Introduction to Algebra"
    description = models.TextField(blank=True)
    week_number = models.PositiveIntegerField(help_text="Expected week of the term to teach this")
    is_completed = models.BooleanField(default=False)

    def __str__(self):
        return self.title