# Generated by Django 4.2.2 on 2023-06-15 05:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('elevators', '0011_alter_elevator_destination_floor'),
    ]

    operations = [
        migrations.AlterField(
            model_name='elevator',
            name='destination_floor',
            field=models.CharField(default='[]', max_length=50),
        ),
    ]
