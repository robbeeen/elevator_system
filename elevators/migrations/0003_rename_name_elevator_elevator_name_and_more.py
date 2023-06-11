# Generated by Django 4.2.2 on 2023-06-11 07:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('elevators', '0002_elevator_direction'),
    ]

    operations = [
        migrations.RenameField(
            model_name='elevator',
            old_name='name',
            new_name='elevator_name',
        ),
        migrations.AlterField(
            model_name='elevator',
            name='current_floor',
            field=models.IntegerField(default=0),
        ),
    ]