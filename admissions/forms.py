from django import forms
from .models import AdmissionApplication

class AdmissionForm(forms.ModelForm):
    class Meta:
        model = AdmissionApplication
        fields = ['first_name', 'last_name', 'date_of_birth', 'gender', 
                 'email', 'parent_phone', 'address', 'grade_applying_for', 'previous_school']
        widgets = {
            'first_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Child\'s First Name'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Child\'s Last Name'}),
            'date_of_birth': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'gender': forms.Select(attrs={'class': 'form-select'}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'parent@example.com'}),
            'parent_phone': forms.TextInput(attrs={'class': 'form-control'}),
            'address': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'grade_applying_for': forms.Select(attrs={'class': 'form-select'}),
            'previous_school': forms.TextInput(attrs={'class': 'form-control'}),
        }