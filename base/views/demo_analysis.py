from django.shortcuts import render, redirect
from django.db.models import Count, Q
from ..models import SocialHistory, UserProfile, MedicalHistory
import json
from functools import wraps

LOCATION_CHOICES = [
    ('BRGY571', 'Barangay 571, Manila'),
    ('BRGY570', 'Barangay 570, Manila'),
    ('BRGY580', 'Barangay 580, Manila'),
    ('BRGY569', 'Barangay 569, Manila'),
    ('BRGY572', 'Barangay 572, Manila'),
    ('BRGY574', 'Barangay 574, Manila'),
    ('BRGY576', 'Barangay 576, Manila'),
    ('FRMMLA', 'From Manila'),
    ('OUTMLA', 'Outside Manila'),
]

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
    # Check if multiple locations have the same highest value
    for item in sorted_data[1:]:
        if item[1] == highest[1]:
            highest = (highest[0] + ", " + item[0], highest[1])  # Concatenate multiple locations
    return highest, sorted_data[-1]

@staff_login_required
def demographics_analysis(request):
    location_stats = []
    for location_code, location_name in LOCATION_CHOICES:
        stats = {
            'location_name': location_name,
            'cough_count': MedicalHistory.objects.filter(user__userprofile__location=location_code, cough_2_weeks=True).count(),
            'tuberculosis_count': MedicalHistory.objects.filter(user__userprofile__location=location_code, pulmonary_tubercolosis=True).count(),
            'smoker_count': SocialHistory.objects.filter(user__userprofile__location=location_code, smoker=True).count(),
            'asthma_count': MedicalHistory.objects.filter(user__userprofile__location=location_code, asthma=True).count(),
            # Add other statistics fields here...
        }
        location_stats.append(stats)

    # Calculate highest and lowest statistics
    cough_highest, cough_lowest = calculate_highest_lowest({stat['location_name']: stat['cough_count'] for stat in location_stats})
    tuberculosis_highest, tuberculosis_lowest = calculate_highest_lowest({stat['location_name']: stat['tuberculosis_count'] for stat in location_stats})
    smoker_highest, smoker_lowest = calculate_highest_lowest({stat['location_name']: stat['smoker_count'] for stat in location_stats})
    asthma_highest, asthma_lowest = calculate_highest_lowest({stat['location_name']: stat['asthma_count'] for stat in location_stats})

    # Prepare data for graphs
    labels = [stat['location_name'] for stat in location_stats]
    cough_counts = [stat['cough_count'] for stat in location_stats]
    tuberculosis_counts = [stat['tuberculosis_count'] for stat in location_stats]
    smoker_counts = [stat['smoker_count'] for stat in location_stats]
    asthma_counts = [stat['asthma_count'] for stat in location_stats]
    # Add other statistics fields here...

    context = {
        'location_stats': location_stats,
        'cough_highest': cough_highest,
        'cough_lowest': cough_lowest,
        'tuberculosis_highest': tuberculosis_highest,
        'tuberculosis_lowest': tuberculosis_lowest,
        'smoker_highest': smoker_highest,
        'smoker_lowest': smoker_lowest,
        'asthma_highest': asthma_highest,
        'asthma_lowest': asthma_lowest,
        'labels': json.dumps(labels),
        'cough_counts': json.dumps(cough_counts),
        'tuberculosis_counts': json.dumps(tuberculosis_counts),
        'smoker_counts': json.dumps(smoker_counts),
        'asthma_counts': json.dumps(asthma_counts),
        # Add other statistics fields to pass to the template...
    }

    return render(request, 'base/staff-section/demographics_analysis.html', context)



from django.shortcuts import render
from datetime import datetime, timedelta
from ..models import User
import json

def patients_analysis(request):
    # Filter non-staff users (patients)
    patients = User.objects.filter(is_staff=False)

    # Get today's date
    today = datetime.now().date()

    # Get start and end date of the current week
    start_of_week = today - timedelta(days=today.weekday())
    end_of_week = start_of_week + timedelta(days=6)

    # Get start and end date of the current month
    start_of_month = today.replace(day=1)
    end_of_month = start_of_month.replace(month=start_of_month.month % 12 + 1, day=1) - timedelta(days=1)

    # Count patients registered per day
    patients_per_day_data = []
    for i in range(7):
        date = today - timedelta(days=i)
        count = patients.filter(date_joined__date=date).count()
        patients_per_day_data.append((date.strftime('%Y-%m-%d'), count))

    # Count patients registered per week for the past few weeks
    patients_per_week_data = []
    for i in range(4):  # Last 4 weeks
        start = start_of_week - timedelta(weeks=i)
        end = start + timedelta(days=6)
        count = patients.filter(date_joined__date__range=[start, end]).count()
        patients_per_week_data.append((f"{start.strftime('%Y-%m-%d')} to {end.strftime('%Y-%m-%d')}", count))

    # Count patients registered per month
    patients_per_month = patients.filter(date_joined__date__range=[start_of_month, end_of_month]).count()

    # Count patients registered today
    patients_today = patients.filter(date_joined__date=today).count()

    # Construct the context data
    context = {
        'patients_per_day_data': json.dumps(patients_per_day_data),
        'patients_per_week_data': json.dumps(patients_per_week_data),
        'patients_today': patients_today,
        'patients_per_week': patients_per_week_data[0][1],  # Current week count
        'patients_per_month': patients_per_month,
    }

    # Render the template with the context data
    return render(request, 'base/staff-section/users_analysis.html', context)