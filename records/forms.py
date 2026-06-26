from django import forms
from .models import Maintenance

class MaintenanceForm(forms.ModelForm):
    class Meta:
        model = Maintenance
        fields = ['vehicle', 'date', 'km', 'next_km', 'description']
        widgets = {
            'date': forms.DateInput(attrs={'type': 'date'}),
        }