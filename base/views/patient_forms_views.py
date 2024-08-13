from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from . .models import  Adult, Child,  Form, Pediatric
from . .forms import UserProfileForm, EconomicNumbersForm, SocialHistoryForm, MedicalHistoryForm,  ChildDetailsForm, NewbornStatusForm, PediatricDetailsForm, ImmunizationHistoryForm,VitalSignsForm, NurseNotesForm, DoctorOrderForm

@login_required(login_url='data_privacy')
def choose_form_view(request):
    return render(request, 'base/patient-section/choose_form.html')

@login_required(login_url='login')
def child_form(request):

    if request.method == 'POST':
        user_profile_form = UserProfileForm(request.POST)
        economic_numbers_form = EconomicNumbersForm(request.POST)
        child_details_form = ChildDetailsForm(request.POST)
        newborn_status_form = NewbornStatusForm(request.POST)
        vital_signs_form = VitalSignsForm(request.POST)
        nurse_notes_form = NurseNotesForm(request.POST)
        doctor_order_form = DoctorOrderForm(request.POST)

        if all(form.is_valid() for form in [user_profile_form, economic_numbers_form, child_details_form, newborn_status_form, vital_signs_form
                                            , nurse_notes_form, doctor_order_form]):
            
            user_profile = user_profile_form.save(commit=False)
            user_profile.user = request.user
            user_profile.save()

            economic_numbers = economic_numbers_form.save(commit=False)
            economic_numbers.user = request.user
            economic_numbers.save()

            child_details = child_details_form.save(commit=False)
            child_details.user = request.user
            child_details.save()

            newborn_status = newborn_status_form.save(commit=False)
            newborn_status.user = request.user
            newborn_status.save()

            vital_signs = vital_signs_form.save(commit=False)
            vital_signs.user = request.user
            vital_signs.save()

            nurse_notes = nurse_notes_form.save(commit=False)
            nurse_notes.user = request.user
            nurse_notes.save() 

            doctor_order = doctor_order_form.save(commit=False)
            doctor_order.user = request.user
            doctor_order.save()

            form_instance = Form.objects.create(
                user=request.user,
                title="Child Form",
                record_type="Child",
                status="Unverified"  
            )

            child_patient = Child.objects.update_or_create(
                user=request.user,
                user_profile=user_profile,
                economic_numbers=economic_numbers,
                child_details=child_details,
                newborn_status=newborn_status,
                doctor_order = doctor_order,
                nurse_notes = nurse_notes,
                vital_signs = vital_signs,
                form=form_instance
            )

            return redirect('user_dashboard')

    else:
        user_profile_form = UserProfileForm()
        economic_numbers_form = EconomicNumbersForm()
        child_details_form = ChildDetailsForm()
        newborn_status_form = NewbornStatusForm()

    context = {
        'user_profile_form': user_profile_form,
        'economic_numbers_form': economic_numbers_form,
        'child_details_form': child_details_form,
        'newborn_status_form': newborn_status_form,
    }

    return render(request, 'base/patient-section/child_form.html', context)

@login_required(login_url='login')
def pediatric_form(request):

    if request.method == 'POST':
        user_profile_form = UserProfileForm(request.POST)
        economic_numbers_form = EconomicNumbersForm(request.POST)
        social_history_form = SocialHistoryForm(request.POST)
        medical_history_form = MedicalHistoryForm(request.POST)
        pediatric_details_form = PediatricDetailsForm(request.POST)
        immunization_history_form = ImmunizationHistoryForm(request.POST)
        vital_signs_form = VitalSignsForm(request.POST)
        nurse_notes_form = NurseNotesForm(request.POST)
        doctor_order_form = DoctorOrderForm(request.POST)

        if all(form.is_valid() for form in [user_profile_form, economic_numbers_form, social_history_form, medical_history_form, pediatric_details_form, immunization_history_form, 
        vital_signs_form, nurse_notes_form, doctor_order_form]):
            
            user_profile = user_profile_form.save(commit=False)
            user_profile.user = request.user
            user_profile.save()

            economic_numbers = economic_numbers_form.save(commit=False)
            economic_numbers.user = request.user
            economic_numbers.save()

            social_history = social_history_form.save(commit=False)
            social_history.user = request.user
            social_history.save()

            medical_history = medical_history_form.save(commit=False)
            medical_history.user = request.user
            medical_history.save()

            pediatric_details = pediatric_details_form.save(commit=False)
            pediatric_details.user = request.user
            pediatric_details.save()

            immunization_history = immunization_history_form.save(commit=False)
            immunization_history.user = request.user
            immunization_history.save()

            nurse_notes = nurse_notes_form.save(commit=False)
            nurse_notes.user = request.user
            nurse_notes.save() 

            doctor_order = doctor_order_form.save(commit=False)
            doctor_order.user = request.user
            doctor_order.save()

            vital_signs = vital_signs_form.save(commit=False)
            vital_signs.user = request.user
            vital_signs.save()

            form_instance = Form.objects.create(
                user=request.user,
                title="Pediatric Form",
                record_type="Pediatric",
                status="Unverified"  
            )

            pediatric_patient = Pediatric.objects.create(
                user=request.user,
                user_profile=user_profile,
                economic_numbers=economic_numbers,
                social_history=social_history,
                medical_history=medical_history,
                pediatric_details=pediatric_details,
                immunization_history=immunization_history,
                doctor_order = doctor_order,
                nurse_notes = nurse_notes,
                vital_signs = vital_signs,
                form=form_instance

            )

            return redirect('user_dashboard')

    else:
        user_profile_form = UserProfileForm()
        economic_numbers_form = EconomicNumbersForm()
        social_history_form = SocialHistoryForm()
        medical_history_form = MedicalHistoryForm()
        pediatric_details_form = PediatricDetailsForm()
        immunization_history_form = ImmunizationHistoryForm()

    context = {
        'user_profile_form': user_profile_form,
        'economic_numbers_form': economic_numbers_form,
        'social_history_form': social_history_form,
        'medical_history_form': medical_history_form,
        'pediatric_details_form': pediatric_details_form,
        'immunization_history_form': immunization_history_form,
    }

    return render(request, 'base/patient-section/pediatric_form.html', context)

@login_required(login_url='login')
def adult_form(request):

    if request.method == 'POST':
        user_profile_form = UserProfileForm(request.POST)
        economic_numbers_form = EconomicNumbersForm(request.POST)
        social_history_form = SocialHistoryForm(request.POST)
        medical_history_form = MedicalHistoryForm(request.POST)
        vital_signs_form = VitalSignsForm(request.POST)
        nurse_notes_form = NurseNotesForm(request.POST)
        doctor_order_form = DoctorOrderForm(request.POST)

        if all(form.is_valid() for form in [user_profile_form, economic_numbers_form, social_history_form, medical_history_form, vital_signs_form
                                            , nurse_notes_form, doctor_order_form]):
            
            user_profile = user_profile_form.save(commit=False)
            user_profile.user = request.user
            user_profile.save()

            economic_numbers = economic_numbers_form.save(commit=False)
            economic_numbers.user = request.user
            economic_numbers.save()

            social_history = social_history_form.save(commit=False)
            social_history.user = request.user
            social_history.save()

            medical_history = medical_history_form.save(commit=False)
            medical_history.user = request.user
            medical_history.save()

            nurse_notes = nurse_notes_form.save(commit=False)
            nurse_notes.user = request.user
            nurse_notes.save() 

            doctor_order = doctor_order_form.save(commit=False)
            doctor_order.user = request.user
            doctor_order.save()
            
            vital_signs = vital_signs_form.save(commit=False)
            vital_signs.user = request.user
            vital_signs.save()

            form_instance = Form.objects.create(
                user=request.user,
                title="Adult Form",
                record_type="Adult",
                status="Unverified"  
            )

            adult_patient = Adult.objects.create(
                user=request.user,
                user_profile=user_profile,
                economic_numbers=economic_numbers,
                social_history=social_history,
                medical_history=medical_history,
                doctor_order = doctor_order,
                nurse_notes = nurse_notes,
                vital_signs = vital_signs,
                form=form_instance
            )

            return redirect('user_dashboard')

    else:
        user_profile_form = UserProfileForm()
        economic_numbers_form = EconomicNumbersForm()
        social_history_form = SocialHistoryForm()
        medical_history_form = MedicalHistoryForm()

    context = {
        'user_profile_form': user_profile_form,
        'economic_numbers_form': economic_numbers_form,
        'social_history_form': social_history_form,
        'medical_history_form': medical_history_form,
    }

    return render(request, 'base/patient-section/adult_form.html', context)