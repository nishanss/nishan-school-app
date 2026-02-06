from django.shortcuts import render, redirect, get_object_or_404
from .models import Curriculum, LessonPlan
from academics.models import Grade
from subjects.models import Subject

def curriculum_list(request):
    grades = Grade.objects.all().prefetch_related('curriculum_set__subject')
    return render(request, 'curriculum/curriculum_list.html', {'grades': grades})

def curriculum_detail(request, pk):
    curriculum = get_object_or_404(Curriculum, pk=pk)
    lessons = curriculum.lessons.all().order_by('week_number')
    return render(request, 'curriculum/curriculum_detail.html', {
        'curriculum': curriculum,
        'lessons': lessons
    })