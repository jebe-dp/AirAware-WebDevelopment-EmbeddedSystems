from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import User, UserProfile, EconomicNumbers, SocialHistory, MedicalHistory, ChildDetails, NewbornStatus, PediatricDetails, ImmunizationHistory, DoctorOrder, NurseNotes, VitalSigns, Announcement
from datetime import date

class DateInput(forms.DateInput):
    input_type = 'date'

class RegistrationForm(UserCreationForm):
    class Meta:
        model = User
        fields = [ 'first_name', 'middle_name', 'last_name'
                  , 'birth_date' , 'username'
                  ]
        
        widgets = {
            'birth_date': DateInput()
        }

class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = '__all__'
        exclude = ['user', 'age']

class EconomicNumbersForm(forms.ModelForm):
    class Meta:
        model = EconomicNumbers
        fields = '__all__'
        exclude = ['user']

class SocialHistoryForm(forms.ModelForm):
    class Meta:
        model = SocialHistory
        fields = '__all__'
        exclude = ['user']

class MedicalHistoryForm(forms.ModelForm):
    class Meta:
        model = MedicalHistory
        fields = '__all__'
        exclude = ['user']

        widgets = {
            'immunization_date': DateInput()
        }

class DoctorOrderForm(forms.ModelForm):
    class Meta:
        model = DoctorOrder
        fields = '__all__'
        exclude = ['user', 'filled_datetime', 'filled_by']

class NurseNotesForm(forms.ModelForm):
    class Meta:
        model = NurseNotes
        fields = '__all__'
        exclude = ['user', 'filled_datetime', 'filled_by']
        widgets = {
            'admission_date': DateInput(),
        }

class VitalSignsForm(forms.ModelForm):
    class Meta:
        model = VitalSigns
        fields = '__all__'
        exclude = ['user', 'filled_by']

class ImmunizationHistoryForm(forms.ModelForm):
    class Meta:
        model = ImmunizationHistory
        fields = '__all__'
        exclude = ['user']
        widgets = {
            'deworm_date': DateInput(),
        }

class PediatricDetailsForm(forms.ModelForm):
    class Meta:
        model = PediatricDetails
        fields = '__all__'
        exclude = ['user']

class ChildDetailsForm(forms.ModelForm):
    class Meta:
        model = ChildDetails
        fields = '__all__'
        exclude = ['user']
        
class NewbornStatusForm(forms.ModelForm):
    class Meta:
        model = NewbornStatus
        fields = '__all__'
        exclude = ['user']
        widgets = {
            'ns_date': DateInput(),
            'bcg_date': DateInput(),
            'dpt_opv_date': DateInput(),
            'pcv_date': DateInput(),
            'ipv_date': DateInput(),
            'hepa_date': DateInput(),
        }

class AnnouncementForm(forms.ModelForm):
    class Meta:
        model = Announcement
        fields = '__all__'
        widgets = {
            'date': DateInput(),
        }