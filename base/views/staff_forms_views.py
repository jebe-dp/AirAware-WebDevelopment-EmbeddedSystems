from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, JsonResponse
from . .models import  Adult, Child,  Form, Pediatric, DoctorOrder, NurseNotes, VitalSigns
from . .forms import DoctorOrderForm, NurseNotesForm, VitalSignsForm
from functools import wraps
import json

def staff_login_required(view_func):
    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect('home')  
        elif not request.user.is_staff:
            return redirect('home')  
        else:
            return view_func(request, *args, **kwargs)
    return wrapper

@staff_login_required
def add_doctor_order(request, form_id):
    form_instance = get_object_or_404(Form, pk=form_id)
    user = form_instance.user
    form = get_object_or_404(Form, pk=form_id)

    if form.record_type == 'Adult':
        adult = get_object_or_404(Adult, form=form)
        nurse_notes = adult.nurse_notes
        vital_signs = adult.vital_signs

        context = {
            'form': form,
            'nurse_notes' : nurse_notes,
            'vital_signs': vital_signs
        }

    elif form.record_type == 'Child':
        child = get_object_or_404(Child, form=form)
        nurse_notes = child.nurse_notes
        vital_signs = child.vital_signs

        context = {
            'form': form,
            'nurse_notes' : nurse_notes,
            'vital_signs': vital_signs
        }

    elif form.record_type == 'Pediatric':
        pediatric = get_object_or_404(Pediatric, form=form)
        nurse_notes = pediatric.nurse_notes
        vital_signs = pediatric.vital_signs

        context = {
            'form': form,
            'nurse_notes' : nurse_notes,
            'vital_signs': vital_signs
        }

    if DoctorOrder.objects.filter(id=form_id).exists():
        existing_order = get_object_or_404(DoctorOrder, id=form_id)
        doctor_order_form = DoctorOrderForm(request.POST or None, instance=existing_order)
    else:
        doctor_order_form = DoctorOrderForm(request.POST or None)
    
    if request.method == 'POST':
        if doctor_order_form.is_valid():
            doctor_order = doctor_order_form.save(commit=False)
            doctor_order.user = form_instance.user
            doctor_order.filled_by = request.user
            doctor_order.save()
            
            form_instance.doctor_order = doctor_order
            form_instance.save()
            
            if form_instance.record_type == 'Adult':
                patient_instance = get_object_or_404(Adult, form=form_instance)
                patient_instance.doctor_order = doctor_order
                patient_instance.save()
            elif form_instance.record_type == 'Pediatric':
                patient_instance = get_object_or_404(Pediatric, form=form_instance)
                patient_instance.doctor_order = doctor_order
                patient_instance.save()
            elif form_instance.record_type == 'Child':
                patient_instance = get_object_or_404(Child, form=form_instance)
                patient_instance.doctor_order = doctor_order
                patient_instance.save()
            
            response_data = {
                'message': 'Doctor Order Successfully Added!'
            }
            return JsonResponse(response_data)
    
    context = {
        'doctor_order_form': doctor_order_form,
        'patient_name': f"{user.first_name} {user.last_name}",
        'nurse_notes': nurse_notes,
        'vital_signs': vital_signs,
    }
    
    return render(request, 'base/staff-section/add_doctor_order.html', context)

@staff_login_required
def add_nurse_notes(request, form_id):
    form_instance = get_object_or_404(Form, pk=form_id)
    user = form_instance.user 

    if NurseNotes.objects.filter(id=form_id).exists():
        existing_notes = get_object_or_404(NurseNotes, id=form_id)
        existing_vital_signs = get_object_or_404(VitalSigns, id=form_id)
        nurse_notes_form = NurseNotesForm(request.POST or None, instance=existing_notes)
        vital_signs_form = VitalSignsForm(request.POST or None, instance=existing_vital_signs)
    else:
        nurse_notes_form = NurseNotesForm(request.POST or None)
        vital_signs_form = VitalSignsForm(request.POST or None)
    
    if request.method == 'POST':
        if nurse_notes_form.is_valid() and vital_signs_form.is_valid():
            nurse_notes = nurse_notes_form.save(commit=False)
            nurse_notes.user = form_instance.user
            nurse_notes.filled_by = request.user
            nurse_notes.save()
            
            vital_signs = vital_signs_form.save(commit=False)
            vital_signs.user = form_instance.user
            vital_signs.filled_by = request.user
            vital_signs.save()
            
            form_instance.nurse_notes = nurse_notes
            form_instance.vital_signs = vital_signs
            form_instance.save()
            
            if form_instance.record_type == 'Adult':
                patient_instance = get_object_or_404(Adult, form=form_instance)
                patient_instance.nurse_notes = nurse_notes
                patient_instance.vital_signs = vital_signs
                patient_instance.save()
            elif form_instance.record_type == 'Pediatric':
                patient_instance = get_object_or_404(Pediatric, form=form_instance)
                patient_instance.nurse_notes = nurse_notes
                patient_instance.vital_signs = vital_signs
                patient_instance.save()
            elif form_instance.record_type == 'Child':
                patient_instance = get_object_or_404(Child, form=form_instance)
                patient_instance.nurse_notes = nurse_notes
                patient_instance.vital_signs = vital_signs
                patient_instance.save()
            
            response_data = {
                'message': 'Nurse Notes Successfully Added!'
            }
            
            return JsonResponse(response_data)  
    
    context = {
        'nurse_notes_form': nurse_notes_form,
        'vital_signs_form': vital_signs_form,
        'patient_name': f"{user.first_name} {user.last_name}",
    }
    
    return render(request, 'base/staff-section/add_nurse_notes.html', context)