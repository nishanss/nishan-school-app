from django.shortcuts import render, redirect
from django.contrib import messages
from academics.models import Section
from students.models import Student
from .models import Attendance
from datetime import date

def mark_attendance(request):
    sections = Section.objects.all()
    selected_section_id = request.GET.get('section')
    selected_date = request.GET.get('date', date.today().isoformat())
    
    students = []
    if selected_section_id:
        students = Student.objects.filter(section_id=selected_section_id, is_active=True)

    if request.method == 'POST':
        # This is where we loop through the students and save the data
        for student in students:
            status = request.POST.get(f'status_{student.id}')
            Attendance.objects.update_or_create(
                student=student,
                date=selected_date,
                defaults={'status': status, 'section_id': selected_section_id}
            )
        messages.success(request, f"Attendance for {selected_date} saved successfully!")
        return redirect('mark_attendance')

    return render(request, 'attendance/mark_attendance.html', {
        'sections': sections,
        'students': students,
        'selected_section': selected_section_id,
        'selected_date': selected_date,
    })