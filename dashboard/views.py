from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from students.models import Student
from academics.models import Grade, Section

@login_required
def index(request):
    context = {
        'total_students': Student.objects.count(),
        'total_grades': Grade.objects.count(),
        'total_sections': Section.objects.count(),
    }
    return render(request, 'dashboard/index.html', context)