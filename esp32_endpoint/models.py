# models.py
from django.db import models
from base.models import User
from django.utils import timezone
from base.models import VitalSigns

class SensorData(models.Model):
    created_at = models.DateTimeField(default=timezone.now, verbose_name='Created At')

    temp = models.FloatField(null=True, verbose_name='Temperature')
    mlx_ambient_temp = models.FloatField(null=True, verbose_name='MLX Ambient Temperature')
    # ds_temp = models.FloatField(null=True, verbose_name='DS Temperature')   
    humidity = models.FloatField(null=True, verbose_name='Humidity')
    heat_index = models.FloatField(null=True, verbose_name='Heat Index')
    air_gases = models.FloatField(null=True, verbose_name='Air Gases')
    pm1 = models.IntegerField(null=True, verbose_name='PM1')
    pm2_5 = models.IntegerField(null=True, verbose_name='PM2.5')
    pm10 = models.IntegerField(null=True, verbose_name='PM10')

    def __str__(self):
        return f'SensorData object ({self.created_at})'
    
class VitalSign(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    pulse_rate = models.IntegerField(null=True, blank=True)
    spo2 = models.IntegerField(null=True, blank=True)
    temperature = models.FloatField(null=True, blank=True)
    respiratory_rate = models.IntegerField(null=True, blank=True)
    systolic_bp = models.IntegerField(null=True, blank=True)
    diastolic_bp = models.IntegerField(null=True, blank=True)
    created_at = models.DateTimeField(default=timezone.now)

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

        latest_vitals = VitalSigns.objects.filter(user=self.user).order_by('-id').first()

        if latest_vitals:
            latest_vitals.pulse_rate = self.pulse_rate
            latest_vitals.blood_oxygen_levels = self.spo2
            latest_vitals.body_temperature = self.temperature
            latest_vitals.respiratory_rate = self.respiratory_rate
            latest_vitals.systolic_bp = self.systolic_bp
            latest_vitals.diastolic_bp = self.diastolic_bp
            latest_vitals.save()
        else:
            VitalSigns.objects.create(
                user=self.user,
                pulse_rate=self.pulse_rate,
                blood_oxygen_levels=self.spo2,
                body_temperature=self.temperature,
                respiratory_rate=self.respiratory_rate,
                systolic_bp=self.systolic_bp,
                diastolic_bp=self.diastolic_bp
            )