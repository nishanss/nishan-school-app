from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .models import AdmissionApplication
from .forms import AdmissionForm
from students.models import Student
from academics.models import Section
from django.core.mail import send_mail

def apply_online(request):
    if request.method == 'POST':
        form = AdmissionForm(request.POST)
        if form.is_valid():
            application = form.save()
            messages.success(request, f"Application for {application.first_name} submitted successfully! We will contact you soon.")
            return redirect('apply_online')
    else:
        form = AdmissionForm()
    
    return render(request, 'admissions/apply_online.html', {'form': form})

@login_required
def admission_list(request):
    applications = AdmissionApplication.objects.filter(status='pending').order_by('-date_applied')
    return render(request, 'admissions/admission_list.html', {'applications': applications})

@login_required
def approve_application(request, pk):
    application = get_object_or_404(AdmissionApplication, pk=pk)
    
    if request.method == 'POST':
        roll_number = request.POST.get('roll_number')
        section_id = request.POST.get('section')
        
        if not roll_number or not section_id:
            messages.error(request, "Please provide a Roll Number and Section to approve.")
            return redirect('admission_detail', pk=pk)
            
        student = Student.objects.create(
            first_name=application.first_name,
            last_name=application.last_name,
            date_of_birth=application.date_of_birth,
            gender=application.gender,
            email=application.email,
            parent_phone=application.parent_phone,
            roll_number=roll_number,
            section_id=section_id,
            is_active=True
        )
        
        application.status = 'approved'
        application.save()

        send_mail(
        subject=f'Admission Approved - {student.first_name}',
        message=f'Congratulations! {student.first_name} has been admitted to {student.section}. Roll Number: {student.roll_number}',
        from_email='nishansanadwayanad@gmail.com',
        recipient_list=[application.email],
        fail_silently=True,
        )
        
        messages.success(request, f"Student {student.first_name} has been officially admitted to Class {student.section}!")
        return redirect('admission_list')

    sections = Section.objects.filter(grade=application.grade_applying_for)
    return render(request, 'admissions/admission_detail.html', {
        'application': application,
        'sections': sections
    })
    
@login_required
def reject_application(request, pk):
    application = get_object_or_404(AdmissionApplication, pk=pk)
    application.status = 'rejected'
    application.save()
    messages.warning(request, "Application rejected.")
    return redirect('admission_list')