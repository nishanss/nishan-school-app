from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .models import Invoice, FeeItem, SalarySlip
from academics.models import Section, Grade
from students.models import Student
from staff.models import Staff
from datetime import date, datetime, timedelta

@login_required
def invoice_list(request):
    status = request.GET.get('status')
    
    invoices = Invoice.objects.all().select_related('student', 'fee_item').order_by('-date_issued')
    
    fee_item_id = request.GET.get('fee_item')
    student_query = request.GET.get('student_name')
    
    if fee_item_id:
        invoices = invoices.filter(fee_item_id=fee_item_id)

    if status:
        invoices = invoices.filter(status=status)

    if student_query:
        invoices = invoices.filter(student__first_name__icontains=student_query) | \
                   invoices.filter(student__last_name__icontains=student_query)
        
    context = {
        'invoices': invoices,
        'fee_items': FeeItem.objects.all(),
        'status_choices': Invoice.STATUS_CHOICES,
        'current_filters': request.GET
    }
    return render(request, 'finance/invoice_list.html', context)

@login_required
def invoice_create_bulk(request):
    if request.method == 'POST':
        grade_id = request.POST.get('grade')
        fee_item_id = request.POST.get('fee_item')
        due_date = request.POST.get('due_date')
        
        if not all([grade_id, fee_item_id, due_date]):
            messages.error(request, "Please select Grade, Fee, and Due Date.")
            return redirect('invoice_create_bulk')

        students = Student.objects.filter(section__grade_id=grade_id, is_active=True)
        fee_item = get_object_or_404(FeeItem, pk=fee_item_id)
        
        created_count = 0
        for student in students:
            Invoice.objects.create(
                student=student,
                fee_item=fee_item,
                amount=fee_item.amount,
                due_date=due_date,
                status='unpaid'
            )
            created_count += 1
            
        messages.success(request, f"Generated {created_count} invoices for {fee_item.name}.")
        return redirect('invoice_list')

    grades = Grade.objects.all()
    fee_items = FeeItem.objects.all()
    default_due = (date.today() + timedelta(days=30)).isoformat()
    
    return render(request, 'finance/invoice_create_bulk.html', {
        'grades': grades,
        'fee_items': fee_items,
        'default_due': default_due
    })

@login_required
def invoice_detail(request, pk):
    invoice = get_object_or_404(Invoice, pk=pk)
    return render(request, 'finance/invoice_detail.html', {'invoice': invoice})

@login_required
def salary_list(request):
    selected_month = request.GET.get('month', date.today().strftime('%Y-%m'))
    
    salaries = SalarySlip.objects.filter(month__startswith=selected_month)
    
    total_payout = sum(s.net_salary for s in salaries)
    pending_count = salaries.filter(status='pending').count()

    context = {
        'salaries': salaries,
        'selected_month': selected_month,
        'total_payout': total_payout,
        'pending_count': pending_count
    }
    return render(request, 'finance/salary_list.html', context)

@login_required
def generate_payroll(request):
    if request.method == 'POST':
        month_str = request.POST.get('month') 
        if not month_str:
            messages.error(request, "Please select a month.")
            return redirect('salary_list')

        year, month = map(int, month_str.split('-'))
        salary_date = date(year, month, 1)

        staff_members = Staff.objects.filter(is_active=True)
        created_count = 0
        
        for staff in staff_members:
            slip, created = SalarySlip.objects.get_or_create(
                staff=staff,
                month=salary_date,
                defaults={
                    'basic_salary': staff.base_salary,
                    'allowances': 0,
                    'deductions': 0,
                    'status': 'pending'
                }
            )
            if created:
                created_count += 1
        
        if created_count > 0:
            messages.success(request, f"Generated payroll for {created_count} staff members!")
        else:
            messages.info(request, "Payroll for this month already exists.")
            
        return redirect('salary_list')

    return redirect('salary_list')

@login_required
def mark_salary_paid(request, pk):
    slip = get_object_or_404(SalarySlip, pk=pk)
    slip.status = 'paid'
    slip.payment_date = date.today()
    slip.save()
    messages.success(request, f"Paid {slip.staff.first_name} successfully!")
    return redirect('salary_list')