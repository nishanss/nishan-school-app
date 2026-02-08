from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from students.models import Student
from academics.models import Grade, Section
from django.db.models import Sum
from attendance.models import Attendance
from finance.models import Invoice
from datetime import date
from django.db.models import Count, Avg
from exams.models import Mark
from admissions.models import AdmissionApplication

# @login_required
# def index(request):
#     context = {
#         'total_students': Student.objects.count(),
#         'total_grades': Grade.objects.count(),
#         'total_sections': Section.objects.count(),
#     }
#     return render(request, 'dashboard/index.html', context)

@login_required
def index(request):
    today = date.today()
    
    total_students = Student.objects.filter(is_active=True).count()
    total_grades = Grade.objects.count() 
    total_sections = Section.objects.count()  
    
    today_attendance = Attendance.objects.filter(date=today)
    present_today = today_attendance.filter(status='present').count()
    attendance_rate = (present_today / total_students * 100) if total_students > 0 else 0
    
    total_invoiced = Invoice.objects.aggregate(Sum('amount'))['amount__sum'] or 0
    total_paid = Invoice.objects.filter(status='paid').aggregate(Sum('amount'))['amount__sum'] or 0
    collection_rate = (total_paid / total_invoiced * 100) if total_invoiced > 0 else 0
    
    top_performing_sections = Section.objects.annotate(
        avg_marks=Avg('students__mark__marks_obtained')
    ).order_by('-avg_marks')[:5]

    recent_admissions = AdmissionApplication.objects.filter(
        status='pending'
    ).order_by('-date_applied')[:5]

    context = {
        'total_students': total_students,
        'total_grades': total_grades,
        'total_sections': total_sections,
        'attendance_rate': round(attendance_rate, 1),
        'total_invoiced': total_invoiced,
        'total_paid': total_paid,
        'outstanding': total_invoiced - total_paid,
        'collection_rate': round(collection_rate, 1),
        'top_performing_sections': top_performing_sections,
        'recent_admissions': recent_admissions,
    }
    return render(request, 'dashboard/index.html', context)