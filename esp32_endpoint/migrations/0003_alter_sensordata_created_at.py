# Generated by Django 5.0.6 on 2024-05-19 17:34

import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('esp32_endpoint', '0002_alter_vitalsign_created_at'),
    ]

    operations = [
        migrations.AlterField(
            model_name='sensordata',
            name='created_at',
            field=models.DateTimeField(default=django.utils.timezone.now, verbose_name='Created At'),
        ),
    ]
