from django import forms # type: ignore
from django.contrib.auth import get_user_model # type: ignore
from django.contrib.auth.forms import UserCreationForm # type: ignore
from django.forms import DateInput # type: ignore
from .models import (
    Department, 
    Staff, 
    Patient, 
    Appointment,  # Make sure this is imported
    Medicine,     # Make sure this is imported
    Prescription
)

class DepartmentForm(forms.ModelForm):
    class Meta:
        model = Department
        fields = ['name', 'head', 'description']
        widgets = {
            'head': forms.Select(attrs={'class': 'form-control'})
        }


class PatientForm(forms.ModelForm):
    class Meta:
        model = Patient
        fields = '__all__'  # or list all fields explicitly
        
    def clean_phone(self):
        phone = self.cleaned_data.get('phone')
        # Add any phone validation logic here
        return phone
        
    def clean_emergency_phone(self):
        emergency_phone = self.cleaned_data.get('emergency_phone')
        # Add any emergency phone validation logic here
        return emergency_phone

User = get_user_model()

class StaffUserCreationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email')

class StaffForm(forms.ModelForm):
    class Meta:
        model = Staff
        fields = '__all__'
        widgets = {
            'hire_date': DateInput(attrs={'type': 'date'}),
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Set date input format
        self.fields['hire_date'].input_formats = ['%Y-%m-%d']
        
        # Add Bootstrap classes to all fields
        for field in self.fields:
            self.fields[field].widget.attrs.update({'class': 'form-control'})
            if field == 'hire_date':
                self.fields[field].widget.attrs.update({'placeholder': 'YYYY-MM-DD'})
class AppointmentForm(forms.ModelForm):
    class Meta:
        model = Appointment
        fields = '__all__'
        widgets = {
            'patient': forms.Select(attrs={'class': 'form-select'}),
            'doctor': forms.Select(attrs={'class': 'form-select'}),
            'department': forms.Select(attrs={'class': 'form-select'}),
            'appointment_date': forms.DateTimeInput(attrs={
                'class': 'form-control',
                'type': 'datetime-local'
            }),
            'status': forms.Select(attrs={'class': 'form-select'}),
            'reason': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3
            }),
            'diagnosis': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3
            }),
            'prescription': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3
            }),
            'notes': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 2
            }),
        }

class MedicineForm(forms.ModelForm):
    class Meta:
        model = Medicine
        fields = '__all__'
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'category': forms.Select(attrs={'class': 'form-select'}),
            'description': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 2
            }),
            'price': forms.NumberInput(attrs={'class': 'form-control'}),
            'quantity_in_stock': forms.NumberInput(attrs={'class': 'form-control'}),
            'manufacturer': forms.TextInput(attrs={'class': 'form-control'}),
            'expiry_date': forms.DateInput(attrs={
                'class': 'form-control',
                'type': 'date'
            }),
        }

class PrescriptionForm(forms.ModelForm):
    class Meta:
        model = Prescription
        fields = '__all__'
        widgets = {
            'appointment': forms.Select(attrs={'class': 'form-select'}),
            'medicine': forms.Select(attrs={'class': 'form-select'}),
            'dosage': forms.TextInput(attrs={'class': 'form-control'}),
            'duration': forms.TextInput(attrs={'class': 'form-control'}),
            'instructions': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3
            }),
        }