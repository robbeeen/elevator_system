from rest_framework import serializers
from .models import Elevator, ElevatorRequest
"""
Serializer  for Elevator
"""


class ElevatorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Elevator
        fields = '__all__'


"""
Serializer for ElevatorRequest
"""


class ElevatorRequestSerializer(serializers.ModelSerializer):
    class Meta:
        model = ElevatorRequest
        fields = '__all__'
