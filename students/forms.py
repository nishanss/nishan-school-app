from django import forms
from .models import Student
from academics.models import Section

class StudentForm(forms.ModelForm):
    class Meta:
        model = Student
        fields = ['first_name', 'last_name', 'roll_number', 'date_of_birth', 'section', 'gender', 'email', 'parent_phone', 'photo', 'is_active']
        # widgets = {
        #     'date_of_birth': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
        # }

        widgets = {
            'first_name': forms.TextInput(attrs={'class': 'form-control'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control'}),
            'date_of_birth': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'roll_number': forms.TextInput(attrs={'class': 'form-control'}),
            'section': forms.Select(attrs={'class': 'form-select'}),
            'gender': forms.Select(attrs={'class': 'form-select'}),
            'email': forms.EmailInput(attrs={'class': 'form-select'}),
            'parent_phone': forms.TextInput(attrs={'class': 'form-select'}),
            'photo': forms.FileInput(attrs={'class': 'form-select'}),
            'is_active': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }

    def clean_photo(self):
        photo = self.cleaned_data.get('photo')
        if photo:
            if photo.size > 5 * 1024 * 1024:
                raise forms.ValidationError("Image file too large ( > 5MB )")
            
            if not photo.name.lower().endswith(('.png', '.jpg', '.jpeg')):
                raise forms.ValidationError("Only PNG, JPG, JPEG allowed")
        
        return photo