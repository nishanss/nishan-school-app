from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from academics.models import Grade
from .models import Subject

@login_required
def subject_list(request):
    grades = Grade.objects.all().prefetch_related('subjects')
    return render(request, 'subjects/subject_list.html', {'grades': grades})