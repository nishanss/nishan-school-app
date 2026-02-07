from django.shortcuts import render, redirect, get_object_or_404
from .models import Student
from .forms import StudentForm
from django.contrib import messages
from django.contrib.auth.decorators import login_required
# from django.db import models
from django.db.models import Q
from academics.models import Section
from django.db.models import Avg
import io
from django.http import HttpResponse
from django.template.loader import get_template
from xhtml2pdf import pisa
from datetime import date
from django.core.paginator import Paginator

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

    paginator = Paginator(students, 50)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    sections = Section.objects.all()
    return render(request, 'students/student_list.html', {
        'students': page_obj, 
        'page_obj': page_obj,
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
    
    attendance = student.attendance_records.all()
    total_days = attendance.count()
    days_present = attendance.filter(status='present').count()
    attendance_pc = (days_present / total_days * 100) if total_days > 0 else 0
    
    marks = student.mark_set.all().select_related('exam__subject')
    avg_score = marks.aggregate(Avg('marks_obtained'))['marks_obtained__avg'] or 0
    
    invoices = student.invoices.all().order_by('-date_issued')
    unpaid_balance = sum(inv.amount for inv in invoices.filter(status='unpaid'))

    return render(request, 'students/student_detail.html', {
        'student': student,
        'attendance_pc': round(attendance_pc, 1),
        'avg_score': round(avg_score, 1),
        'marks': marks,
        'invoices': invoices,
        'unpaid_balance': unpaid_balance,
    })

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

@login_required
def download_report_card(request, pk):
    student = get_object_or_404(Student, pk=pk)
    
    marks = student.mark_set.all().select_related('exam__subject')
    avg_score = marks.aggregate(Avg('marks_obtained'))['marks_obtained__avg'] or 0
    
    attendance = student.attendance_records.all()
    days_present = attendance.filter(status='present').count()
    total_days = attendance.count()
    attendance_pc = (days_present / total_days * 100) if total_days > 0 else 0

    template_path = 'students/report_card_pdf.html'
    context = {
        'student': student,
        'marks': marks,
        'avg_score': round(avg_score, 2),
        'attendance_pc': round(attendance_pc, 1),
        'today': date.today(),
    }
    
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="{student.roll_number}_report.pdf"'
    
    template = get_template(template_path)
    html = template.render(context)

    pisa_status = pisa.CreatePDF(html, dest=response)
    
    if pisa_status.err:
       return HttpResponse('We had some errors <pre>' + html + '</pre>')
    return response