# Generated by Django 5.0.6 on 2024-06-10 10:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0015_user_location'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='user',
            name='location',
        ),
        migrations.AddField(
            model_name='userprofile',
            name='location',
            field=models.CharField(blank=True, choices=[('BRGY571', 'Barangay 571, Manila'), ('BRGY570', 'Barangay 570, Manila'), ('BRGY580', 'Barangay 580, Manila'), ('BRGY569', 'Barangay 569, Manila'), ('BRGY572', 'Barangay 572, Manila'), ('BRGY574', 'Barangay 574, Manila'), ('BRGY576', 'Barangay 576, Manila'), ('FRMMLA', 'From Manila'), ('OUTMLA', 'Outside Manila')], default='', max_length=10),
        ),
    ]
