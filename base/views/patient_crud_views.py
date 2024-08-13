from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.template.loader import get_template
from . .models import Adult, Child,  Form, Pediatric
from . .forms import UserProfileForm, EconomicNumbersForm, SocialHistoryForm, MedicalHistoryForm,  ChildDetailsForm, NewbornStatusForm, PediatricDetailsForm, ImmunizationHistoryForm
from xhtml2pdf import pisa

@login_required(login_url='home')
def patient_view_form(request, form_id):
    user = request.user
    form = Form.objects.get(pk=form_id, user=user)

    if form.record_type == 'Adult':
        adult = Adult.objects.get(form=form, user=user)
        user_profile = adult.user_profile
        economic_numbers = adult.economic_numbers
        social_history = adult.social_history
        medical_history = adult.medical_history
        doctor_order = adult.doctor_order
        nurse_notes = adult.nurse_notes
        vital_signs = adult.vital_signs

        context = {
            'form': form,
            'user_profile': user_profile,
            'economic_numbers': economic_numbers,
            'social_history': social_history,
            'medical_history': medical_history,
            'doctor_order': doctor_order,
            'nurse_notes' : nurse_notes,
            'vital_signs': vital_signs
        }

    elif form.record_type == 'Child':
        child = get_object_or_404(Child, form=form, user=user)
        user_profile = child.user_profile
        child_details = child.child_details
        newborn_status = child.newborn_status
        economic_numbers = child.economic_numbers
        doctor_order = child.doctor_order
        nurse_notes = child.nurse_notes
        vital_signs = child.vital_signs

        context = {
            'form': form,
            'user_profile': user_profile,
            'child_details': child_details,
            'newborn_status': newborn_status,
            'economic_numbers': economic_numbers,
            'doctor_order': doctor_order,
            'nurse_notes' : nurse_notes,
            'vital_signs': vital_signs
        }

    elif form.record_type == 'Pediatric':
        pediatric = get_object_or_404(Pediatric, form=form, user=user)
        user_profile = pediatric.user_profile
        pediatric_details = pediatric.pediatric_details
        immunization_history = pediatric.immunization_history
        social_history = pediatric.social_history
        medical_history = pediatric.medical_history
        economic_numbers = pediatric.economic_numbers
        doctor_order = pediatric.doctor_order
        nurse_notes = pediatric.nurse_notes
        vital_signs = pediatric.vital_signs

        context = {
            'form': form,
            'user_profile': user_profile,
            'pediatric_details': pediatric_details,
            'immunization_history': immunization_history,
            'social_history': social_history,
            'medical_history': medical_history,
            'economic_numbers': economic_numbers,
            'doctor_order': doctor_order,
            'nurse_notes' : nurse_notes,
            'vital_signs': vital_signs
        }

    return render(request, 'base/patient-section/patient_view_form.html', context)



@login_required(login_url='home')
def patient_update_form(request, form_id):
    user = request.user
    form = get_object_or_404(Form, pk=form_id, user=user)

    if form.record_type == 'Adult':
        adult = get_object_or_404(Adult, form=form, user=user)
        user_profile = adult.user_profile
        economic_numbers = adult.economic_numbers
        social_history = adult.social_history
        medical_history = adult.medical_history

        if request.method == 'POST':
            user_profile_form = UserProfileForm(request.POST, instance=user_profile)
            economic_numbers_form = EconomicNumbersForm(request.POST, instance=economic_numbers)
            social_history_form = SocialHistoryForm(request.POST, instance=social_history)
            medical_history_form = MedicalHistoryForm(request.POST, instance=medical_history)

            if all(form.is_valid() for form in [user_profile_form, economic_numbers_form, social_history_form, medical_history_form]):
                user_profile_form.save()
                economic_numbers_form.save()
                social_history_form.save()
                medical_history_form.save()
                return redirect('patient_view_form', form_id=form_id)
        else:
            user_profile_form = UserProfileForm(instance=user_profile)
            economic_numbers_form = EconomicNumbersForm(instance=economic_numbers)
            social_history_form = SocialHistoryForm(instance=social_history)
            medical_history_form = MedicalHistoryForm(instance=medical_history)

        context = {
            'form': form,
            'user_profile_form': user_profile_form,
            'economic_numbers_form': economic_numbers_form,
            'social_history_form': social_history_form,
            'medical_history_form': medical_history_form,
        }

        return render(request, 'base/patient-section/patient_update_form.html', context)

    elif form.record_type == 'Child':
        child = get_object_or_404(Child, form=form, user=user)
        user_profile = child.user_profile
        child_details = child.child_details
        newborn_status = child.newborn_status
        economic_numbers = child.economic_numbers

        if request.method == 'POST':
            user_profile_form = UserProfileForm(request.POST, instance=user_profile)
            child_details_form = ChildDetailsForm(request.POST, instance=child_details)
            newborn_status_form = NewbornStatusForm(request.POST, instance=newborn_status)
            economic_numbers_form = EconomicNumbersForm(request.POST, instance=economic_numbers)

            if all(form.is_valid() for form in [user_profile_form, child_details_form, newborn_status_form, economic_numbers_form]):
                user_profile_form.save()
                child_details_form.save()
                newborn_status_form.save()
                economic_numbers_form.save()
                return redirect('patient_view_form', form_id=form_id)
        else:
            user_profile_form = UserProfileForm(instance=user_profile)
            child_details_form = ChildDetailsForm(instance=child_details)
            newborn_status_form = NewbornStatusForm(instance=newborn_status)
            economic_numbers_form = EconomicNumbersForm(instance=economic_numbers)

        context = {
            'form': form,
            'user_profile_form': user_profile_form,
            'child_details_form': child_details_form,
            'newborn_status_form': newborn_status_form,
            'economic_numbers_form': economic_numbers_form,
        }

        return render(request, 'base/patient-section/patient_update_form.html', context)

    elif form.record_type == 'Pediatric':
        pediatric = get_object_or_404(Pediatric, form=form, user=user)
        user_profile = pediatric.user_profile
        pediatric_details = pediatric.pediatric_details
        immunization_history = pediatric.immunization_history
        social_history = pediatric.social_history
        medical_history = pediatric.medical_history
        economic_numbers = pediatric.economic_numbers

        if request.method == 'POST':
            user_profile_form = UserProfileForm(request.POST, instance=user_profile)
            pediatric_details_form = PediatricDetailsForm(request.POST, instance=pediatric_details)
            immunization_history_form = ImmunizationHistoryForm(request.POST, instance=immunization_history)
            social_history_form = SocialHistoryForm(request.POST, instance=social_history)
            medical_history_form = MedicalHistoryForm(request.POST, instance=medical_history)
            economic_numbers_form = EconomicNumbersForm(request.POST, instance=economic_numbers)

            if all(form.is_valid() for form in [user_profile_form, pediatric_details_form, immunization_history_form, social_history_form, medical_history_form, economic_numbers_form]):
                user_profile_form.save()
                pediatric_details_form.save()
                immunization_history_form.save()
                social_history_form.save()
                medical_history_form.save()
                economic_numbers_form.save()
                return redirect('patient_view_form', form_id=form_id)
        else:
            user_profile_form = UserProfileForm(instance=user_profile)
            pediatric_details_form = PediatricDetailsForm(instance=pediatric_details)
            immunization_history_form = ImmunizationHistoryForm(instance=immunization_history)
            social_history_form = SocialHistoryForm(instance=social_history)
            medical_history_form = MedicalHistoryForm(instance=medical_history)
            economic_numbers_form = EconomicNumbersForm(instance=economic_numbers)

        context = {
            'form': form,
            'user_profile_form': user_profile_form,
            'pediatric_details_form': pediatric_details_form,
            'immunization_history_form': immunization_history_form,
            'social_history_form': social_history_form,
            'medical_history_form': medical_history_form,
            'economic_numbers_form': economic_numbers_form,
        }

        return render(request, 'base/patient-section/patient_update_form.html', context)
    
@login_required(login_url='home')
def patient_delete_form(request, form_id):
    user = request.user
    form = get_object_or_404(Form, pk=form_id, user=user)

    if form.record_type == 'Adult':
        adult = get_object_or_404(Adult, form=form, user=user)
        adult.user_profile.delete()
        adult.economic_numbers.delete()
        adult.social_history.delete()
        adult.medical_history.delete()
        adult.delete()
    elif form.record_type == 'Child':
        child = get_object_or_404(Child, form=form, user=user)
        child.user_profile.delete()
        child.economic_numbers.delete()
        child.child_details.delete()
        child.newborn_status.delete()
        child.delete()
    elif form.record_type == 'Pediatric':
        pediatric = get_object_or_404(Pediatric, form=form, user=user)
        pediatric.user_profile.delete()
        pediatric.economic_numbers.delete()
        pediatric.social_history.delete()
        pediatric.medical_history.delete()
        pediatric.pediatric_details.delete()
        pediatric.immunization_history.delete()
        pediatric.delete()

    form.delete()

    return redirect('user_dashboard')

@login_required(login_url='home')
def generate_pdf(request, form_id):
    form = get_object_or_404(Form, pk=form_id)
    user = request.user

    if form.record_type == 'Adult':
        adult = get_object_or_404(Adult, form=form, user=user)
        user_profile = adult.user_profile
        economic_numbers = adult.economic_numbers
        social_history = adult.social_history
        medical_history = adult.medical_history
        doctor_order = adult.doctor_order
        nurse_notes = adult.nurse_notes
        vital_signs = adult.vital_signs

        context = {
            'form': form,
            'user_profile': user_profile,
            'economic_numbers': economic_numbers,
            'social_history': social_history,
            'medical_history': medical_history,
            'doctor_order' : doctor_order,
            'nurse_notes' : nurse_notes,
            'vital_signs' : vital_signs,
        }

    elif form.record_type == 'Child':
        child = get_object_or_404(Child, form=form, user=user)
        user_profile = child.user_profile
        child_details = child.child_details
        newborn_status = child.newborn_status
        economic_numbers = child.economic_numbers
        doctor_order = child.doctor_order
        nurse_notes = child.nurse_notes
        vital_signs = child.vital_signs

        context = {
            'form': form,
            'user_profile': user_profile,
            'child_details': child_details,
            'newborn_status': newborn_status,
            'economic_numbers': economic_numbers,
            'doctor_order' : doctor_order,
            'nurse_notes' : nurse_notes,
            'vital_signs' : vital_signs,
        }

    elif form.record_type == 'Pediatric':
        pediatric = get_object_or_404(Pediatric, form=form, user=user)
        user_profile = pediatric.user_profile
        pediatric_details = pediatric.pediatric_details
        immunization_history = pediatric.immunization_history
        social_history = pediatric.social_history
        medical_history = pediatric.medical_history
        economic_numbers = pediatric.economic_numbers
        doctor_order = pediatric.doctor_order
        nurse_notes = pediatric.nurse_notes
        vital_signs = pediatric.vital_signs

        context = {
            'form': form,
            'user_profile': user_profile,
            'pediatric_details': pediatric_details,
            'immunization_history': immunization_history,
            'social_history': social_history,
            'medical_history': medical_history,
            'economic_numbers': economic_numbers,
            'doctor_order' : doctor_order,
            'nurse_notes' : nurse_notes,
            'vital_signs' : vital_signs,
        }

    html_template = get_template('base/patient-section/patient_view_form.html')
    html = html_template.render(context)

    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="HealthRecord_{form_id}.pdf"'

    pisa_status = pisa.CreatePDF(html, dest=response)
    if pisa_status.err:
        return HttpResponse('An error occurred while generating the PDF')

    return response