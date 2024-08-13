from django.shortcuts import render, redirect
from ..models import SocialHistory, UserProfile, MedicalHistory
import json
from functools import wraps

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

def calculate_highest_lowest(data):
    sorted_data = sorted(data.items(), key=lambda x: x[1], reverse=True)
    highest = sorted_data[0]
    # Check if multiple age groups have the same highest value
    for item in sorted_data[1:]:
        if item[1] == highest[1]:
            highest = (highest[0] + ", " + item[0], highest[1])  # Concatenate multiple age groups
    return highest, sorted_data[-1]


@staff_login_required
def social_history_analysis(request):
   
    smoker_age_groups = {
        '0-20': SocialHistory.objects.filter(smoker=True, user__userprofile__age__lte=20).values('user').distinct().count(),
        '20-40': SocialHistory.objects.filter(smoker=True, user__userprofile__age__gt=20, user__userprofile__age__lte=40).values('user').distinct().count(),
        '40-60': SocialHistory.objects.filter(smoker=True, user__userprofile__age__gt=40, user__userprofile__age__lte=60).values('user').distinct().count(),
        '60+': SocialHistory.objects.filter(smoker=True, user__userprofile__age__gt=60).values('user').distinct().count(),
    }

    smoker_gender = {
        'Male': SocialHistory.objects.filter(smoker=True, user__userprofile__sex='Male').values('user').distinct().count(),
        'Female': SocialHistory.objects.filter(smoker=True, user__userprofile__sex='Female').values('user').distinct().count(),
    }

    prohibited_drugs_age_groups = {
        '0-20': SocialHistory.objects.filter(prohibited_drug=True, user__userprofile__age__lte=20).values('user').distinct().count(),
        '20-40': SocialHistory.objects.filter(prohibited_drug=True, user__userprofile__age__gt=20, user__userprofile__age__lte=40).values('user').distinct().count(),
        '40-60': SocialHistory.objects.filter(prohibited_drug=True, user__userprofile__age__gt=40, user__userprofile__age__lte=60).values('user').distinct().count(),
        '60+': SocialHistory.objects.filter(prohibited_drug=True, user__userprofile__age__gt=60).values('user').distinct().count(),
    }

    prohibited_drugs_gender = {
        'Male': SocialHistory.objects.filter(prohibited_drug=True, user__userprofile__sex='Male').values('user').distinct().count(),
        'Female': SocialHistory.objects.filter(prohibited_drug=True, user__userprofile__sex='Female').values('user').distinct().count(),
    }

    alcohol_intake_age_groups = {
        '0-20': SocialHistory.objects.filter(alcohol_intake=True, user__userprofile__age__lte=20).values('user').distinct().count(),
        '20-40': SocialHistory.objects.filter(alcohol_intake=True, user__userprofile__age__gt=20, user__userprofile__age__lte=40).values('user').distinct().count(),
        '40-60': SocialHistory.objects.filter(alcohol_intake=True, user__userprofile__age__gt=40, user__userprofile__age__lte=60).values('user').distinct().count(),
        '60+': SocialHistory.objects.filter(alcohol_intake=True, user__userprofile__age__gt=60).values('user').distinct().count(),
    }

    alcohol_intake_gender = {
        'Male': SocialHistory.objects.filter(alcohol_intake=True, user__userprofile__sex='Male').values('user').distinct().count(),
        'Female': SocialHistory.objects.filter(alcohol_intake=True, user__userprofile__sex='Female').values('user').distinct().count(),
    }

    # Calculate highest and lowest for each category
    smoker_highest, smoker_lowest = calculate_highest_lowest(smoker_age_groups)
    smoker_g_highest, smoker_g_lowest = calculate_highest_lowest(smoker_gender)

    prohibited_drugs_highest, prohibited_drugs_lowest = calculate_highest_lowest(prohibited_drugs_age_groups)
    prohibited_drugs_g_highest, prohibited_drugs_g_lowest = calculate_highest_lowest(prohibited_drugs_gender)

    alcohol_intake_highest, alcohol_intake_lowest = calculate_highest_lowest(alcohol_intake_age_groups)
    alcohol_intake_g_highest, alcohol_intake_g_lowest = calculate_highest_lowest(alcohol_intake_gender)

    context = {
        'smoker_age_groups': json.dumps(smoker_age_groups),
        'smoker_gender': json.dumps(smoker_gender),
        'prohibited_drugs_age_groups': json.dumps(prohibited_drugs_age_groups),
        'prohibited_drugs_gender': json.dumps(prohibited_drugs_gender),
        'alcohol_intake_age_groups': json.dumps(alcohol_intake_age_groups),
        'alcohol_intake_gender': json.dumps(alcohol_intake_gender),
        'smoker_highest': smoker_highest,
        'smoker_lowest': smoker_lowest,
        'smoker_g_highest': smoker_g_highest,
        'smoker_g_lowest': smoker_g_lowest,
        'prohibited_drugs_highest': prohibited_drugs_highest,
        'prohibited_drugs_lowest': prohibited_drugs_lowest,
        'prohibited_drugs_g_highest': prohibited_drugs_g_highest,
        'prohibited_drugs_g_lowest': prohibited_drugs_g_lowest,
        'alcohol_intake_highest': alcohol_intake_highest,
        'alcohol_intake_lowest': alcohol_intake_lowest,
        'alcohol_intake_g_highest': alcohol_intake_g_highest,
        'alcohol_intake_g_lowest': alcohol_intake_g_lowest,
    }


    return render(request, 'base/staff-section/social_analysis.html', context)

@staff_login_required
def medical_history_analysis(request):
    
    diabetes_age_groups = {
        '0-20': MedicalHistory.objects.filter(diabetes=True, user__userprofile__age__lte=20).values('user').distinct().count(),
        '20-40': MedicalHistory.objects.filter(diabetes=True, user__userprofile__age__gt=20, user__userprofile__age__lte=40).values('user').distinct().count(),
        '40-60': MedicalHistory.objects.filter(diabetes=True, user__userprofile__age__gt=40, user__userprofile__age__lte=60).values('user').distinct().count(),
        '60+': MedicalHistory.objects.filter(diabetes=True, user__userprofile__age__gt=60).values('user').distinct().count(),
    }

    diabetes_gender = {
        'Male': MedicalHistory.objects.filter(diabetes=True, user__userprofile__sex='Male').values('user').distinct().count(),
        'Female': MedicalHistory.objects.filter(diabetes=True, user__userprofile__sex='Female').values('user').distinct().count(),
    }

  
    asthma_age_groups = {
        '0-20': MedicalHistory.objects.filter(asthma=True, user__userprofile__age__lte=20).values('user').distinct().count(),
        '20-40': MedicalHistory.objects.filter(asthma=True, user__userprofile__age__gt=20, user__userprofile__age__lte=40).values('user').distinct().count(),
        '40-60': MedicalHistory.objects.filter(asthma=True, user__userprofile__age__gt=40, user__userprofile__age__lte=60).values('user').distinct().count(),
        '60+': MedicalHistory.objects.filter(asthma=True, user__userprofile__age__gt=60).values('user').distinct().count(),
    }

    asthma_gender = {
        'Male': MedicalHistory.objects.filter(asthma=True, user__userprofile__sex='Male').values('user').distinct().count(),
        'Female': MedicalHistory.objects.filter(asthma=True, user__userprofile__sex='Female').values('user').distinct().count(),
    }


    hypertension_age_groups = {
        '0-20': MedicalHistory.objects.filter(hypertension=True, user__userprofile__age__lte=20).values('user').distinct().count(),
        '20-40': MedicalHistory.objects.filter(hypertension=True, user__userprofile__age__gt=20, user__userprofile__age__lte=40).values('user').distinct().count(),
        '40-60': MedicalHistory.objects.filter(hypertension=True, user__userprofile__age__gt=40, user__userprofile__age__lte=60).values('user').distinct().count(),
        '60+': MedicalHistory.objects.filter(hypertension=True, user__userprofile__age__gt=60).values('user').distinct().count(),
    }

    hypertension_gender = {
        'Male': MedicalHistory.objects.filter(hypertension=True, user__userprofile__sex='Male').values('user').distinct().count(),
        'Female': MedicalHistory.objects.filter(hypertension=True, user__userprofile__sex='Female').values('user').distinct().count(),
    }

    pulmonary_tuberculosis_age_groups = {
        '0-20': MedicalHistory.objects.filter(pulmonary_tubercolosis=True, user__userprofile__age__lte=20).values('user').distinct().count(),
        '20-40': MedicalHistory.objects.filter(pulmonary_tubercolosis=True, user__userprofile__age__gt=20, user__userprofile__age__lte=40).values('user').distinct().count(),
        '40-60': MedicalHistory.objects.filter(pulmonary_tubercolosis=True, user__userprofile__age__gt=40, user__userprofile__age__lte=60).values('user').distinct().count(),
        '60+': MedicalHistory.objects.filter(pulmonary_tubercolosis=True, user__userprofile__age__gt=60).values('user').distinct().count(),
    }

    pulmonary_tuberculosis_gender = {
        'Male': MedicalHistory.objects.filter(pulmonary_tubercolosis=True, user__userprofile__sex='Male').values('user').distinct().count(),
        'Female': MedicalHistory.objects.filter(pulmonary_tubercolosis=True, user__userprofile__sex='Female').values('user').distinct().count(),
    }

    cancer_age_groups = {
        '0-20': MedicalHistory.objects.filter(cancer=True, user__userprofile__age__lte=20).values('user').distinct().count(),
        '20-40': MedicalHistory.objects.filter(cancer=True, user__userprofile__age__gt=20, user__userprofile__age__lte=40).values('user').distinct().count(),
        '40-60': MedicalHistory.objects.filter(cancer=True, user__userprofile__age__gt=40, user__userprofile__age__lte=60).values('user').distinct().count(),
        '60+': MedicalHistory.objects.filter(cancer=True, user__userprofile__age__gt=60).values('user').distinct().count(),
    }

    cancer_gender = {
        'Male': MedicalHistory.objects.filter(cancer=True, user__userprofile__sex='Male').values('user').distinct().count(),
        'Female': MedicalHistory.objects.filter(cancer=True, user__userprofile__sex='Female').values('user').distinct().count(),
    }

    cough_2_weeks_age_groups = {
        '0-20': MedicalHistory.objects.filter(cough_2_weeks=True, user__userprofile__age__lte=20).values('user').distinct().count(),
        '20-40': MedicalHistory.objects.filter(cough_2_weeks=True, user__userprofile__age__gt=20, user__userprofile__age__lte=40).values('user').distinct().count(),
        '40-60': MedicalHistory.objects.filter(cough_2_weeks=True, user__userprofile__age__gt=40, user__userprofile__age__lte=60).values('user').distinct().count(),
        '60+': MedicalHistory.objects.filter(cough_2_weeks=True, user__userprofile__age__gt=60).values('user').distinct().count(),
    }

    cough_2_weeks_gender = {
        'Male': MedicalHistory.objects.filter(cough_2_weeks=True, user__userprofile__sex='Male').values('user').distinct().count(),
        'Female': MedicalHistory.objects.filter(cough_2_weeks=True, user__userprofile__sex='Female').values('user').distinct().count(),
    }

   
    diabetes_age_groups_json = json.dumps(diabetes_age_groups)
    diabetes_gender_json = json.dumps(diabetes_gender)
    asthma_age_groups_json = json.dumps(asthma_age_groups)
    asthma_gender_json = json.dumps(asthma_gender)
    hypertension_age_groups_json = json.dumps(hypertension_age_groups)
    hypertension_gender_json = json.dumps(hypertension_gender)
    pulmonary_tuberculosis_age_groups_json = json.dumps(pulmonary_tuberculosis_age_groups)
    pulmonary_tuberculosis_gender_json = json.dumps(pulmonary_tuberculosis_gender)
    cancer_age_groups_json = json.dumps(cancer_age_groups)
    cancer_gender_json = json.dumps(cancer_gender)
    cough_2_weeks_age_groups_json = json.dumps(cough_2_weeks_age_groups)
    cough_2_weeks_gender_json = json.dumps(cough_2_weeks_gender)

    diabetes_highest, diabetes_lowest = calculate_highest_lowest(diabetes_age_groups)
    diabetes_g_highest, diabetes_g_lowest = calculate_highest_lowest(diabetes_gender)

    asthma_highest, asthma_lowest = calculate_highest_lowest(asthma_age_groups)
    asthma_g_highest, asthma_g_lowest = calculate_highest_lowest(asthma_gender)

    hypertension_highest, hypertension_lowest = calculate_highest_lowest(hypertension_age_groups)
    hypertension_g_highest, hypertension_g_lowest = calculate_highest_lowest(hypertension_gender)

    pulmonary_tuberculosis_highest, pulmonary_tuberculosis_lowest = calculate_highest_lowest(pulmonary_tuberculosis_age_groups)
    pulmonary_tuberculosis_g_highest, pulmonary_tuberculosis_g_lowest = calculate_highest_lowest(pulmonary_tuberculosis_gender)

    cancer_highest, cancer_lowest = calculate_highest_lowest(cancer_age_groups)
    cancer_g_highest, cancer_g_lowest = calculate_highest_lowest(cancer_gender)

    cough_2_weeks_highest, cough_2_weeks_lowest = calculate_highest_lowest(cough_2_weeks_age_groups)
    cough_2_weeks_g_highest, cough_2_weeks_g_lowest = calculate_highest_lowest(cough_2_weeks_gender)

    context = {
        'diabetes_age_groups': json.dumps(diabetes_age_groups),
        'diabetes_gender': json.dumps(diabetes_gender),
        'asthma_age_groups': json.dumps(asthma_age_groups),
        'asthma_gender': json.dumps(asthma_gender),
        'hypertension_age_groups': json.dumps(hypertension_age_groups),
        'hypertension_gender': json.dumps(hypertension_gender),
        'pulmonary_tuberculosis_age_groups': json.dumps(pulmonary_tuberculosis_age_groups),
        'pulmonary_tuberculosis_gender': json.dumps(pulmonary_tuberculosis_gender),
        'cancer_age_groups': json.dumps(cancer_age_groups),
        'cancer_gender': json.dumps(cancer_gender),
        'cough_2_weeks_age_groups': json.dumps(cough_2_weeks_age_groups),
        'cough_2_weeks_gender': json.dumps(cough_2_weeks_gender),
        'diabetes_highest': diabetes_highest,
        'diabetes_lowest': diabetes_lowest,
        'diabetes_g_highest': diabetes_g_highest,
        'diabetes_g_lowest': diabetes_g_lowest,
        'asthma_highest': asthma_highest,
        'asthma_lowest': asthma_lowest,
        'asthma_g_highest': asthma_g_highest,
        'asthma_g_lowest': asthma_g_lowest,
        'hypertension_highest': hypertension_highest,
        'hypertension_lowest': hypertension_lowest,
        'hypertension_g_highest': hypertension_g_highest,
        'hypertension_g_lowest': hypertension_g_lowest,
        'pulmonary_tuberculosis_highest': pulmonary_tuberculosis_highest,
        'pulmonary_tuberculosis_lowest': pulmonary_tuberculosis_lowest,
        'pulmonary_tuberculosis_g_highest': pulmonary_tuberculosis_g_highest,
        'pulmonary_tuberculosis_g_lowest': pulmonary_tuberculosis_g_lowest,
        'cancer_highest': cancer_highest,
        'cancer_lowest': cancer_lowest,
        'cancer_g_highest': cancer_g_highest,
        'cancer_g_lowest': cancer_g_lowest,
        'cough_2_weeks_highest': cough_2_weeks_highest,
        'cough_2_weeks_lowest': cough_2_weeks_lowest,
        'cough_2_weeks_g_highest': cough_2_weeks_g_highest,
        'cough_2_weeks_g_lowest': cough_2_weeks_g_lowest,
    }


    return render(request, 'base/staff-section/medical_analysis.html', context)

