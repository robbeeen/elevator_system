# Generated by Django 4.2.2 on 2023-06-13 06:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('elevators', '0006_remove_elevator_is_operational'),
    ]

    operations = [
        migrations.AlterField(
            model_name='elevatorrequest',
            name='request_type',
            field=models.CharField(choices=[('door', 'DOOR'), ('elevator_working_status', 'ELEVATOR WORKING STATUS'), ('floor', 'FLOOR')], max_length=50),
        ),
        migrations.AlterField(
            model_name='elevatorrequest',
            name='working_status',
            field=models.CharField(choices=[('working', 'WORKING'), ('not_working', 'NOT WORKING'), ('in_maintenance', 'IN_MAINTENANCE')], max_length=50),
        ),
    ]