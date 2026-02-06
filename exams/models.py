from django.db import models
from students.models import Student
from academics.models import Section
from subjects.models import Subject

class Exam(models.Model):
    EXAM_TYPES = (
        ('monthly', 'Monthly Test'),
        ('midterm', 'Mid-Term'),
        ('final', 'Final Exam'),
    )

    name = models.CharField(max_length=100)
    exam_type = models.CharField(max_length=20, choices=EXAM_TYPES)
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE)
    section = models.ForeignKey(Section, on_delete=models.CASCADE)
    date = models.DateField()
    max_marks = models.PositiveIntegerField(default=100)
    passing_marks = models.PositiveIntegerField(default=33)

    def __str__(self):
        return f"{self.name} - {self.subject.name} ({self.section})"

class Mark(models.Model):
    exam = models.ForeignKey(Exam, on_delete=models.CASCADE, related_name='marks')
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    marks_obtained = models.DecimalField(max_digits=5, decimal_places=2)
    remarks = models.CharField(max_length=255, blank=True)

    class Meta:
        unique_together = ('exam', 'student')

    def __str__(self):
        return f"{self.student} - {self.exam.name}: {self.marks_obtained}"