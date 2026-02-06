from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from students.models import Student
from academics.models import Grade, Section
from django.db.models import Sum
from attendance.models import Attendance
from finance.models import Invoice
from datetime import date

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
    
    present_today = Attendance.objects.filter(date=today, status='present').count()
    attendance_rate = (present_today / total_students * 100) if total_students > 0 else 0
    
    total_invoiced = Invoice.objects.aggregate(Sum('amount'))['amount__sum'] or 0
    total_paid = Invoice.objects.filter(status='paid').aggregate(Sum('amount'))['amount__sum'] or 0
    collection_rate = (total_paid / total_invoiced * 100) if total_invoiced > 0 else 0
    
    context = {
        'total_students': total_students,
        'total_grades': total_grades,
        'total_sections': total_sections,
        'attendance_rate': round(attendance_rate, 1),
        'total_invoiced': total_invoiced,
        'total_paid': total_paid,
        'outstanding': total_invoiced - total_paid,
        'collection_rate': round(collection_rate, 1),
    }
    return render(request, 'dashboard/index.html', context)