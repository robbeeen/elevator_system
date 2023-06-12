from django.shortcuts import render
from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.views import APIView

from elevators.models import Elevator, ElevatorRequest
from elevators.serializers import ElevatorSerializer


class CreateElevators(APIView):
    def post(self, request, *args, **kwargs):
        no_of_elevators = request.data.get('no_of_elevators')
        if no_of_elevators and no_of_elevators != 0 and no_of_elevators is not None:
            try:
                no_of_elevators = int(no_of_elevators)
            except ValueError:
                return Response(status=status.HTTP_400_BAD_REQUEST)
            if no_of_elevators > 0:
                for _ in range(no_of_elevators):
                    Elevator.objects.create()
                return Response(status=status.HTTP_201_CREATED)
            else:
                return Response(status=status.HTTP_400_BAD_REQUEST)


class ElevatorsController(viewsets.ModelViewSet):
    queryset = Elevator.objects.all()
    serializer_class = ElevatorSerializer

    @action(detail=True, methods=['GET'])
    def get_elevator_data(self, request, *args, **kwargs):
        try:
            elevator = Elevator.objects.get(id=kwargs.get('pk'))
        except Elevator.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        if request.data.get("type") == "destination_floor":
            data = {"type": request.data.get("type"),
                    "next_destination": elevator.destination_floor}
            return Response(data, status=status.HTTP_200_OK)
        elif request.data.get("type") == "direction":
            data = {"type": request.data.get("type"),
                    "direction": elevator.direction}
            return Response(data, status=status.HTTP_200_OK)
        elif request.data.get("type") == "working_status":
            data = {"type": request.data.get("type"),
                    "working_status": elevator.working_status}
            return Response(data, status=status.HTTP_200_OK)
        elif request.data.get("type") == "door_status":
            data = {"type": request.data.get("type"),
                    "door_status": elevator.door_status}
            return Response(data, status=status.HTTP_200_OK)
        else:
            return Response(status=status.HTTP_400_BAD_REQUEST)

    @action(detail=True, methods=['patch'])
    def update_elevator_data(self, request, *args, **kwargs):
        instance = self.get_object()
        if request.data.get("request_type") == 'door_status':
            data = super().update(request, partial=True)
            print("444444444444444444")
            print(data)
            ElevatorRequest.objects.create(
                elevator=instance, door_status=data.door_status,
                request_type="door"
            )
            return Response({"message": "Status changed successfully.",
                             "Door_status": data.door_status}, status=status.HTTP_200_OK)
