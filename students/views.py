from django.shortcuts import render, redirect, get_object_or_404
from .models import Student
from .forms import StudentForm
from django.contrib import messages
from django.contrib.auth.decorators import login_required
# from django.db import models
from django.db.models import Q
from academics.models import Section

@login_required
def student_list(request):

    query = request.GET.get('q', '').strip()
    section_id = request.GET.get('section', '')
    students = Student.objects.all()

    if query:
        students = Student.objects.filter(
            Q(first_name__icontains=query) | 
            Q(last_name__icontains=query) |
            Q(roll_number__icontains=query)
        )
    # else:
    #     students = Student.objects.all()

    # return render(request, 'students/student_list.html', {'students': students,'query': query})

    if section_id:
        students = students.filter(section_id=section_id)

    sections = Section.objects.all()
    return render(request, 'students/student_list.html', {
        'students': students, 
        'sections': sections,
        'current_section': section_id,
        'query': query,
    })


@login_required
def student_create(request):
    if request.method == "POST":
        form = StudentForm(request.POST, request.FILES) 
        if form.is_valid():
            # form.save()
            student = form.save(commit=False)
            student.created_by = request.user
            student.save()

            messages.success(request, "Student profile created successfully!")
            return redirect('student_list') 
    else:
        form = StudentForm()
    
    return render(request, 'students/student_form.html', {'form': form})

@login_required
def student_detail(request, pk):
    student = get_object_or_404(Student, pk=pk)
    return render(request, 'students/student_detail.html', {'student': student})

@login_required
def student_update(request, pk):
    student = get_object_or_404(Student, pk=pk)
    if request.method == "POST":
        form = StudentForm(request.POST, request.FILES, instance=student)
        if form.is_valid():
            form.save()
            messages.success(request, "Student records - updated.")
            return redirect('student_detail', pk=pk)
    else:
        form = StudentForm(instance=student)
    return render(request, 'students/student_form.html', {'form': form, 'student': student, 'edit_mode': True})

@login_required
def student_delete(request, pk):
    student = get_object_or_404(Student, pk=pk)
    if request.method == "POST":
        student.delete()
        messages.warning(request, f"Student {student.first_name} has been removed.")
        return redirect('student_list')
    
    return render(request, 'students/student_confirm_delete.html', {'student': student})