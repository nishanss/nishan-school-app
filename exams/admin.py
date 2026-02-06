from django.contrib import admin
from .models import Exam, Mark

@admin.register(Exam)
class ExamAdmin(admin.ModelAdmin):
    list_display = ('name', 'subject', 'section', 'date', 'max_marks')
    list_filter = ('exam_type', 'section', 'subject')

@admin.register(Mark)
class MarkAdmin(admin.ModelAdmin):
    list_display = ('student', 'exam', 'marks_obtained')
    list_filter = ('exam__name', 'exam__section')