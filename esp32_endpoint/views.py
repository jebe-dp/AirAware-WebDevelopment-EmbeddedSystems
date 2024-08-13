import requests
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.dates import DateFormatter, AutoDateLocator

from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.views.generic import ListView
from .forms import AuthorizationForm
from .models import SensorData
from django.http import JsonResponse

from django.conf import settings
from HCRecords.config import VITAL_SIGNS_RESOURCE_URL


def temp_diff_graph(request):
    sensor_data = SensorData.objects.all()
    return render(request, 'esp32_endpoint/temp_comparison.html', {'sensor_data': sensor_data})


class SensorDataListView(ListView):
    model = SensorData
    template_name = 'esp32_endpoint/envi_data_raw.html'
    context_object_name = 'data_list'
    paginate_by = 50

    def get_queryset(self):
        # Get the queryset and order it by the 'created_at' field in descending order
        queryset = super().get_queryset().order_by('-created_at')
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        field_names = [field.name for field in SensorData._meta.fields]
        context['field_names'] = field_names
        return context


def realtime_envi_data(request):
    return render(request, 'esp32_endpoint/envi_data_realtime.html')

from django.utils.timezone import localtime
def latest_envi_data(request):
    latest_data = SensorData.objects.latest('created_at')
    local_time = localtime(latest_data.created_at)
    formatted_time = local_time.strftime('%B %d, %Y %I:%M %p')

    data = {
        'created_at': formatted_time,
        'temp': latest_data.temp,
        'heat_index': latest_data.heat_index,
        'humidity': latest_data.humidity,
        'air_gases': latest_data.air_gases,
        'pm1': latest_data.pm1,
        'pm2_5': latest_data.pm2_5,
        'pm10': latest_data.pm10,
    }
    return JsonResponse(data)

def graph_data(request, year=None, month=None, day=None):
    # Set the timezone for matplotlib
    matplotlib.rcParams.update({'timezone': settings.TIME_ZONE})

    # Retrieve all SensorData objects
    data = SensorData.objects.all()

    # Filter data based on provided year, month, and day
    if year:
        data = data.filter(created_at__year=year)
        if month:
            data = data.filter(created_at__month=month)
            if day:
                data = data.filter(created_at__day=day)

    # Check if there is any data available
    if data.exists():
        # Get the field names and their verbose names, excluding id and created_at
        field_names_verbose = {
            field.name: field.verbose_name
            for field in SensorData._meta.fields
            if field.name not in ['id', 'created_at']
        }

        # Create an empty list to store graph data
        graphs = []

        # Loop through each field
        for field_name, verbose_name in field_names_verbose.items():
            # Extract data for the field
            field_data = [getattr(entry, field_name) for entry in data]
            created_at_data = [entry.created_at for entry in data]  # No timezone conversion

            filtered_field_data = [value for value in field_data if value is not None]
            if filtered_field_data:
                avg_value = sum(filtered_field_data) / len(filtered_field_data)
                high_value = max(filtered_field_data)
                high_time = created_at_data[field_data.index(high_value)]
                low_value = min(filtered_field_data)
                low_time = created_at_data[field_data.index(low_value)]
            else:
                # If there are no valid values, set them to None
                avg_value = None
                high_value = None
                high_time = None
                low_value = None
                low_time = None

            # Create the graph with tiny dots
            plt.plot(created_at_data, field_data, linestyle='', marker='o', markersize=2)
            plt.xlabel('Time')
            plt.ylabel(verbose_name)

            # Set the x-axis date and time format
            plt.gca().xaxis.set_major_formatter(DateFormatter('%m-%d-%Y %I:%M %p'))

            # Set automatic date and time tick locator
            plt.gca().xaxis.set_major_locator(AutoDateLocator())

            # Rotate x-axis labels for better readability
            plt.xticks(rotation=45)

            # Increase the plot area size to prevent cropping of x-axis labels
            plt.gcf().autofmt_xdate()

            # Construct the filename for the temporary graph
            graph_filename = f'{settings.MEDIA_ROOT}/graphs/{field_name}_graph.png'

            # Save the temporary graph to a file
            plt.savefig(graph_filename)

            # Get the URL for the saved image file
            graph_url = f'{settings.MEDIA_URL}graphs/{field_name}_graph.png'

            # Store the graph data in the list
            graphs.append({
                'url': graph_url,
                'title': verbose_name,
                'avg_value': round(avg_value, 2) if avg_value is not None else None,
                'high_value': high_value,
                'high_time': high_time,
                'low_value': low_value,
                'low_time': low_time
            })

            # Clear the current plot for the next iteration
            plt.clf()

        # Pass the graphs to the template
        context = {'graphs': graphs}
    else:
        # No data available, set graphs to None
        context = {'graphs': None}

    return render(request, 'esp32_endpoint/multi_graph.html', context)


#
from .forms import VitalSignForm
from .models import VitalSign


# @login_required
# def authorization_form(request):
#     return render(request, 'esp32_endpoint/authorization_form.html')

from django.core.serializers.json import DjangoJSONEncoder
import json
from django.contrib import messages

from .forms import VitalSignForm
from .models import VitalSign
from base.models import VitalSigns

@login_required(login_url='login')
def add_vital_signs(request):
    if request.method == 'POST':
        form = VitalSignForm(request.POST)
        if form.is_valid():
            vital_sign = form.save(commit=False)
            vital_sign.user = request.user
            
            vital_sign.save()
            messages.success(request, "Vital signs recorded successfully.")

            return redirect('add_vital_signs')
        else:
            for error in form.errors.values():
                messages.error(request, error.as_text())
    else:
        form = VitalSignForm()

    user_vital_signs = VitalSign.objects.filter(user=request.user).order_by('-created_at')
    user_vital_signs_data = json.dumps(list(user_vital_signs.values()), cls=DjangoJSONEncoder)

    return render(request, 'esp32_endpoint/add_vital_signs.html', {
        'form': form,
        'vital_signs': user_vital_signs,
        'vital_signs_data': user_vital_signs_data
    })

@login_required
def handle_auth_request(request):
    response_message = None
    status = 'error'
    time_left = 0  # default value
    pulse_rate = ''
    spo2 = ''
    skin_temp = ''

    if request.method == 'POST':
        mutable_data = request.POST.copy()
        if 'request_auth' in request.POST:
            form_without_auth_code = AuthorizationForm(request.POST)
            if form_without_auth_code.is_valid():
                sensor_type = form_without_auth_code.cleaned_data['sensor_type']
                response = send_request_to_vital_signs_endpoint(
                    user_id=request.user.id,
                    first_name=request.user.first_name,
                    last_name=request.user.last_name,
                    sensor_type=sensor_type,
                    auth_code=False
                )
                response_message = response.text
                if response.status_code == 200:
                    status = 'success'
                    response_data = response.json()
                    time_left = response_data.get('time_left', 0)
                    response_message = ""
                else:
                    response_message = response.text
            else:
                response_message = "Invalid Form."
        elif 'submit_auth' in request.POST:
            form_with_auth_code = AuthorizationForm(mutable_data)
            if form_with_auth_code.is_valid():
                auth_code = form_with_auth_code.cleaned_data['authorization_code']
                sensor_type = form_with_auth_code.cleaned_data['sensor_type']
                response = send_request_to_vital_signs_endpoint(
                    user_id=request.user.id,
                    first_name=request.user.first_name,
                    last_name=request.user.last_name,
                    sensor_type=sensor_type,
                    auth_code=auth_code
                )
                response_message = response.text
                if response.status_code == 200:
                    status = 'success'
                    response_data = response.json()
                    if sensor_type == "max":
                        pulse_rate = response_data.get('pulse_rate', '')
                        spo2 = response_data.get('spo2', '')
                    elif sensor_type == "mlx":
                        skin_temp = response_data.get('object_temp', '')
                    time_left = response_data.get('time_left', 0)
                    response_message = ""
                else:
                    response_message = response.text
            else:
                response_message = "Invalid Form."

    return JsonResponse({
        'response_message': response_message if response_message else "",
        'status': status,
        'time_left': time_left,
        'pulse_rate': pulse_rate,
        'spo2': spo2,
        'skin_temp': skin_temp
    })

def send_request_to_vital_signs_endpoint(user_id, first_name, last_name, sensor_type, auth_code=None):
    data = {
        'requester_id': user_id,
        'first_name': first_name,
        'last_name': last_name,
        'sensor_type': sensor_type
    }
    if auth_code:
        data['auth_code'] = auth_code
    
    headers = {'Content-Type': 'application/x-www-form-urlencoded'}
    
    response = requests.post(VITAL_SIGNS_RESOURCE_URL, data=data, headers=headers)
    
    return response