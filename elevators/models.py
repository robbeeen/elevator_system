import uuid

from django.db import models


class Elevator(models.Model):
    STATUS_CHOICES = (
        ("available", "AVAILABLE"),
        ("busy", "BUSY")
    )

    DIRECTION = (
        ("up", "UP"),
        ("down", "DOWN")
    )

    RUNNING_STATUS = (
        ("start", "START"),
        ("stop", "STOP")
    )

    DOOR_STATUS = (
        ("open", "OPEN"),
        ("close", "CLOSE")
    )

    elevator_name = models.CharField(max_length=100, blank=False)
    current_floor = models.IntegerField(default=0, blank=False)
    destination_floor = models.IntegerField(default=0, blank=False)
    is_operational = models.BooleanField(default=True)
    running_status = models.CharField(max_length=50, choices=RUNNING_STATUS, default="start")
    door_status = models.CharField(max_length=50, choices=DOOR_STATUS, default="open")
    status = models.CharField(max_length=50, choices=STATUS_CHOICES, default="available")
    direction = models.CharField(max_length=50, choices=DIRECTION, default="up")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.elevator_name

    def save(self, *args, **kwargs):
        if self.pk is None:
            self.elevator_name = str(uuid.uuid4())  # Convert UUID to string
            super().save(*args, **kwargs)


class ElevatorRequest(models.Model):
    DOOR_STATUS = (
        ("open", "OPEN"),
        ("close", "CLOSE")
    )

    REQUEST_TYPE = (
        ("door", "DOOR"),
        ("elevator", "ELEVATOR"),
        ("floor", "FLOOR")
    )

    elevator = models.ForeignKey(Elevator, on_delete=models.CASCADE)
    current_floor = models.IntegerField(blank=True, null=True)
    destination_floor = models.IntegerField(blank=True, null=True)
    door_status = models.CharField(max_length=50, choices=DOOR_STATUS)
    request_type = models.CharField(max_length=50, choices=REQUEST_TYPE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'request on {self.elevator.elevator_name} at {self.updated_at}'