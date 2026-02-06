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

        existing_attendance = Attendance.objects.filter(
            date=selected_date, 
            section_id=selected_section_id
        ).values_list('student_id', 'status')

        attendance_dict = dict(existing_attendance)

        for student in students:
            student.current_status = attendance_dict.get(student.id, 'present')

    if request.method == 'POST':
        for student in students:
            status = request.POST.get(f'status_{student.id}')
            Attendance.objects.update_or_create(
                student=student,
                date=selected_date,
                defaults={'status': status, 'section_id': selected_section_id}
            )
        messages.success(request, f"Attendance for {selected_date} saved successfully!")
        return redirect(f"{request.path}?section={selected_section_id}&date={selected_date}")

    return render(request, 'attendance/mark_attendance.html', {
        'sections': sections,
        'students': students,
        'selected_section': selected_section_id,
        'selected_date': selected_date,
    })