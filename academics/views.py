from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Grade, Section

@login_required
def academic_dashboard(request):
    grades = Grade.objects.all().prefetch_related('sections')
    return render(request, 'academics/dashboard.html', {'grades': grades})

@login_required
def section_detail(request, pk):
    section = get_object_or_404(Section, pk=pk)
    students = section.students.all()
    return render(request, 'academics/section_detail.html', {'section': section, 'students': students})