from django.db import models
from django.core.exceptions import ValidationError
from academics.models import Section
from subjects.models import Subject
from staff.models import Staff

class TimeSlot(models.Model):
    
    name = models.CharField(max_length=50, help_text="e.g. Period 1, Lunch Break")
    start_time = models.TimeField()
    end_time = models.TimeField()
    is_break = models.BooleanField(default=False)

    class Meta:
        ordering = ['start_time']

    def __str__(self):
        return f"{self.name} ({self.start_time} - {self.end_time})"

class TimetableEntry(models.Model):
    DAYS_OF_WEEK = [
        (1, 'Monday'),
        (2, 'Tuesday'),
        (3, 'Wednesday'),
        (4, 'Thursday'),
        (5, 'Friday'),
        (6, 'Saturday'),
        (7, 'Sunday'),
    ]

    day = models.PositiveSmallIntegerField(choices=DAYS_OF_WEEK)
    time_slot = models.ForeignKey(TimeSlot, on_delete=models.CASCADE)
    section = models.ForeignKey(Section, on_delete=models.CASCADE, related_name='timetable')
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE)
    teacher = models.ForeignKey(Staff, on_delete=models.CASCADE, limit_choices_to={'role': 'TEACHER'})

    class Meta:
        verbose_name_plural = "Timetable Entries"
        unique_together = ('day', 'time_slot', 'section')

    def __str__(self):
        return f"{self.get_day_display()} - {self.time_slot.name}: {self.subject.name} ({self.section.name})"

    def clean(self):
        conflicts = TimetableEntry.objects.filter(
            day=self.day,
            time_slot=self.time_slot,
            teacher=self.teacher
        ).exclude(pk=self.pk)

        if conflicts.exists():
            raise ValidationError(
                f"Teacher {self.teacher} is already assigned to {conflicts.first().section} during this time"
            )