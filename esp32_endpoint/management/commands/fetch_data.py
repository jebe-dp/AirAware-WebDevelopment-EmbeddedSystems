# fetch_data.py
import requests
import time
from django.core.management.base import BaseCommand
from esp32_endpoint.models import SensorData
from HCRecords.config import ENVIRONMENT_RESOURCE_URL

class Command(BaseCommand):
    help = 'Fetch data from a certain resource every 5 seconds and save it to the database'

    def handle(self, *args, **options):
        while True:
            try:
                # Make HTTP GET request to the resource
                response = requests.get(ENVIRONMENT_RESOURCE_URL)
                response.raise_for_status()  # Raise HTTPError for bad status codes
                response_json = response.json()

                # Extract desired keys from JSON response
                mlx_ambient_temp = response_json.get('mlx_ambient_temp')
                ds_temp = response_json.get('ds_temp')

                # Round off -273.1499939 to two decimal places
                rounded_ambient_temp = round(mlx_ambient_temp, 2) if mlx_ambient_temp is not None else None

                sensor_data_fields = {
                    'temp': round(float(response_json.get('temp', None)), 2) if response_json.get('temp') is not None else None,
                    'humidity': round(float(response_json.get('humidity', None)), 2) if response_json.get('humidity') is not None else None,
                    'heat_index': round(float(response_json.get('heat_index', None)), 2) if response_json.get('heat_index') is not None else None,
                    'air_gases': round(float(response_json.get('air_gases', None)), 2) if response_json.get('air_gases') is not None else None,
                    'pm1': int(response_json.get('pm1', None)) if response_json.get('pm1') != 4294967295 else None,
                    'pm2_5': int(response_json.get('pm2_5', None)) if response_json.get('pm2_5') != 4294967295 else None,
                    'pm10': int(response_json.get('pm10', None)) if response_json.get('pm10') != 4294967295 else None,
                    'mlx_ambient_temp': None if rounded_ambient_temp == -273.15 else rounded_ambient_temp,
                    # 'ds_temp': None if ds_temp is None or ds_temp == -127 else round(float(ds_temp), 2)
                }

                # Check if all fields are None
                if not all(value is None for value in sensor_data_fields.values()):
                    # Save extracted data to database
                    sensor_data = SensorData(**sensor_data_fields)
                    sensor_data.save()
                    self.stdout.write(self.style.SUCCESS('Data saved successfully'))
                else:
                    self.stdout.write(self.style.WARNING('All fields are null, data not saved'))

            except requests.RequestException as e:
                self.stderr.write(self.style.ERROR(f'An error occurred: {e}'))

            time.sleep(5)  # Wait for x seconds before making the next request