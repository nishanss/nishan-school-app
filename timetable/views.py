from django.shortcuts import render
from .models import TimeSlot, TimetableEntry
from academics.models import Section, Grade
from staff.models import Staff

def timetable_view(request):
    grade_id = request.GET.get('grade')
    section_id = request.GET.get('section')
    staff_id = request.GET.get('staff')

    grades = Grade.objects.all()

    if grade_id:
        sections = Section.objects.filter(grade_id=grade_id)
    else:
        sections = Section.objects.all()

    time_slots = TimeSlot.objects.all()
    sections = Section.objects.all()
    teachers = Staff.objects.filter(role='TEACHER')
    days = TimetableEntry.DAYS_OF_WEEK
    entries = TimetableEntry.objects.all()

    if grade_id:
        entries = entries.filter(section__grade_id=grade_id)
    if section_id:
        entries = entries.filter(section_id=section_id)
    if staff_id:
        entries = entries.filter(teacher_id=staff_id)

    schedule_map = {}
    for entry in entries:
        schedule_map[(entry.time_slot_id, entry.day)] = entry

    return render(request, 'timetable/timetable_grid.html', {
        'time_slots': time_slots,
        'days': days,
        'schedule_map': schedule_map,
        'grades': grades,
        'sections': sections,
        'teachers': teachers,
        'selected_grade': int(grade_id) if grade_id else None,
        'selected_section': int(section_id) if section_id else None,
        'selected_staff': int(staff_id) if staff_id else None,
    })