# forms.py

from django import forms
from .models import VitalSign

class AuthorizationForm(forms.Form):
    AUTH_CODE_LENGTH = 6
    SENSOR_TYPES = [('mlx', 'Skin Temperature'), ('max', 'Pulse Rate and Blood Oxygen Level')]
    
    sensor_type = forms.ChoiceField(label='Sensor Type', choices=SENSOR_TYPES)
    authorization_code = forms.IntegerField(label='Authorization Code', min_value=0, max_value=999999, required=False)

class VitalSignForm(forms.ModelForm):
    class Meta:
        model = VitalSign
        fields = [
            'pulse_rate', 'spo2', 'temperature',
            'respiratory_rate', 'systolic_bp', 'diastolic_bp'
        ]
        widgets = {
            'pulse_rate': forms.NumberInput(attrs={'id': 'pulse-rate'}),
            'spo2': forms.NumberInput(attrs={'id': 'spo2'}),
            'temperature': forms.NumberInput(attrs={'id': 'temperature'}),
            'respiratory_rate': forms.NumberInput(attrs={'id': 'respiratory-rate'}),
            'systolic_bp': forms.NumberInput(attrs={'id': 'systolic-bp'}),
            'diastolic_bp': forms.NumberInput(attrs={'id': 'diastolic-bp'}),
        }

    def clean(self):
        cleaned_data = super().clean()
        pulse_rate = cleaned_data.get("pulse_rate")
        spo2 = cleaned_data.get("spo2")
        temperature = cleaned_data.get("temperature")
        respiratory_rate = cleaned_data.get("respiratory_rate")
        systolic_bp = cleaned_data.get("systolic_bp")
        diastolic_bp = cleaned_data.get("diastolic_bp")

        if (systolic_bp and not diastolic_bp) or (diastolic_bp and not systolic_bp):
            raise forms.ValidationError("Both systolic and diastolic blood pressure values must be provided.")
        

        if not any([pulse_rate, spo2, temperature, respiratory_rate, systolic_bp, diastolic_bp]):
            raise forms.ValidationError("At least one field must be filled out.")

        return cleaned_data