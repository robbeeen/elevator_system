# Generated by Django 4.2.2 on 2023-06-14 07:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('elevators', '0010_alter_elevator_destination_floor_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='elevator',
            name='destination_floor',
            field=models.CharField(default='', max_length=50),
        ),
    ]
