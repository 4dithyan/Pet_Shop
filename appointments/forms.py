from django import forms
from .models import Appointment

class AppointmentForm(forms.ModelForm):
    """
    Form for creating appointments
    """
    class Meta:
        model = Appointment
        fields = ['service_type', 'pet_name', 'appointment_date', 'appointment_time', 'notes']
        widgets = {
            'service_type': forms.Select(attrs={'class': 'form-select'}),
            'pet_name': forms.TextInput(attrs={'class': 'form-control'}),
            'appointment_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'appointment_time': forms.TimeInput(attrs={'class': 'form-control', 'type': 'time'}),
            'notes': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        }
