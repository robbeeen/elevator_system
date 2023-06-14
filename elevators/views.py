from django.shortcuts import render
from rest_framework import status, viewsets
import json
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.views import APIView

from elevators.models import Elevator, ElevatorRequest
from elevators.serializers import ElevatorSerializer, ElevatorRequestSerializer


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
            updated_data = super().update(request, partial=True)
            ElevatorRequest.objects.create(
                elevator=instance, door_status=updated_data.data['door_status'],
                request_type="door"
            )
            return Response({"message": "Status changed successfully.",
                             "Door_status": updated_data.data['door_status']}, status=status.HTTP_200_OK)

        elif request.data.get("request_type") == 'working_status':
            updated_data = super().update(request, partial=True)
            ElevatorRequest.objects.create(
                elevator=instance, working_status=updated_data.data['working_status'],
                request_type="elevator_working_status"
            )
            return Response({"message": "Status changed successfully.",
                             "Working_status": updated_data.data['working_status']}, status=status.HTTP_200_OK)

    @action(detail=True, methods=['GET'])
    def get_elevator_requests(self, request, *args, **kwargs):
        try:
            elevator = Elevator.objects.get(id=kwargs.get('pk'))
        except Elevator.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        elevator_requests = ElevatorRequest.objects.filter(elevator=elevator)
        serializer = ElevatorRequestSerializer(elevator_requests, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @action(detail=True, methods=['POST'])
    def change_floor(self, request, *args, **kwargs):
        import pdb; pdb.set_trace()
        try:
            destination_floor = int(request.POST.get('destination_floor'))
            if destination_floor:
                elevator = Elevator.objects.get(id=kwargs.get('pk'))
                if destination_floor == elevator.current_floor:
                    print("do nothing")
                    return Response({"message": "destination floor is same as current floor"},
                                    status=status.HTTP_400_BAD_REQUEST)
                else:
                    if destination_floor > elevator.current_floor:
                        if elevator.door_status == 'OPEN':
                            print("close the door")
                        else:
                            self.update_elevator_object(
                                direction="UP", destination_floor=destination_floor,
                                elevator=elevator)
                    else:
                        if elevator.door_status == 'OPEN':
                            print("close the door")
                        else:
                            self.update_elevator_object(
                                direction="DOWN", destination_floor=destination_floor,
                                elevator=elevator)
                ElevatorRequest.objects.create(
                    elevator=elevator, destination_floor=destination_floor,
                    request_type="floor")

        except Elevator.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        elevator.destination_floor = request.data.get('destination_floor')
        elevator.save()
        return Response(status=status.HTTP_200_OK)

    @staticmethod
    def update_elevator_object(direction: str, destination_floor: int, elevator: Elevator):
        elevator.direction = direction
        elevator_destination = json.loads(elevator.destination_floor)
        if isinstance(elevator_destination, list):
            elevator_destination.append(destination_floor)
        else:
            elevator_destination = [destination_floor]
        elevator.destination_floor = json.dumps(elevator_destination)
        elevator.save()
        return Response(status=status.HTTP_200_OK)

