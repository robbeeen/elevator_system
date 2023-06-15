import uuid

from django.db import models


class Elevator(models.Model):
    """
    Elevator model
    """

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

    WORKING_STATUS = (
        ("working", "WORKING"),
        ("not_working", "NOT WORKING"),
        ("in_maintenance", "IN_MAINTENANCE")
    )

    DOOR_STATUS = (
        ("open", "OPEN"),
        ("close", "CLOSE")
    )

    elevator_name = models.CharField(max_length=100, blank=False)
    current_floor = models.IntegerField(default=0, blank=False)
    destination_floor = models.CharField(max_length=50, default="[]", blank=False)
    working_status = models.CharField(max_length=50, choices=WORKING_STATUS, default="working")
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
    """
    Elevator request model for storing the request data into a separate model
    """

    DOOR_STATUS = (
        ("open", "OPEN"),
        ("close", "CLOSE")
    )

    REQUEST_TYPE = (
        ("door", "DOOR"),
        ("elevator_working_status", "ELEVATOR WORKING STATUS"),
        ("floor", "FLOOR")
    )

    WORKING_STATUS = (
        ("working", "WORKING"),
        ("not_working", "NOT WORKING"),
        ("in_maintenance", "IN_MAINTENANCE")
    )

    elevator = models.ForeignKey(Elevator, on_delete=models.CASCADE)
    current_floor = models.IntegerField(blank=True, null=True)
    destination_floor = models.IntegerField(blank=True, null=True)
    door_status = models.CharField(max_length=50, choices=DOOR_STATUS)
    request_type = models.CharField(max_length=50, choices=REQUEST_TYPE)
    working_status = models.CharField(max_length=50, choices=WORKING_STATUS)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'request on {self.elevator.elevator_name} at {self.updated_at}'
