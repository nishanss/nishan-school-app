from django.shortcuts import render, redirect
from django.contrib import messages
from .models import Staff
from .forms import StaffForm
from django.shortcuts import get_object_or_404

def staff_list(request):
    staff_members = Staff.objects.all()
    return render(request, 'staff/staff_list.html', {'staff_members': staff_members})

def staff_create(request):
    if request.method == 'POST':
        form = StaffForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Staff member added successfully.")
            return redirect('staff_list')
    else:
        form = StaffForm()
    return render(request, 'staff/staff_form.html', {'form': form})

def staff_detail(request, pk):
    staff = get_object_or_404(Staff, pk=pk)
    return render(request, 'staff/staff_detail.html', {'staff': staff})