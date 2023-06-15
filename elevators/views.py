import json

from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.views import APIView
import requests
from elevators.models import Elevator, ElevatorRequest
from elevators.serializers import ElevatorSerializer, ElevatorRequestSerializer


class CreateElevators(APIView):
    """
    API for creating N elevators objects
    """

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
    """
    for managing elevators objects
    """
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

    """
    Some additional api for covering the edge cases
    """
    @action(detail=True, methods=['POST'])
    def change_floor(self, request, *args, **kwargs):
        try:
            destination_floor = int(request.POST.get('destination_floor'))
            if destination_floor:
                elevator = Elevator.objects.get(id=kwargs.get('pk'))
                if destination_floor == elevator.current_floor:
                    return Response({"message": "destination floor is same as current floor"},
                                    status=status.HTTP_400_BAD_REQUEST)
                else:
                    if destination_floor > elevator.current_floor:
                        if elevator.door_status == 'open':
                            r = requests.patch(
                                "http://127.0.0.1:8000/elevator/data/{}/update_elevator_data/".format(elevator.id),
                                data={"door_status": "close",
                                      "request_type": "door_status"})

                            if r.status_code == 200:
                                self.update_elevator(
                                    direction="UP", destination_floor=destination_floor,
                                    elevator=elevator)
                            else:
                                return Response({
                                    'message': "Invalid Request Door is not closed"},
                                    status=status.HTTP_400_BAD_REQUEST)
                        else:
                            self.update_elevator(
                                direction="UP", destination_floor=destination_floor,
                                elevator=elevator)
                    else:
                        if elevator.door_status == 'open':
                            r = requests.patch(
                                "http://127.0.0.1:8000/elevator/data/{}/update_elevator_data/".format(elevator.id),
                                data={"door_status": "close",
                                      "request_type": "door_status"})

                            if r.status_code == 200:
                                self.update_elevator(
                                    direction="UP", destination_floor=destination_floor,
                                    elevator=elevator)
                            else:
                                return Response({
                                    'message': "Invalid Request Door is not closed"},
                                    status=status.HTTP_400_BAD_REQUEST)
                        else:
                            self.update_elevator(
                                direction="DOWN", destination_floor=destination_floor,
                                elevator=elevator)
                ElevatorRequest.objects.create(
                    elevator=elevator, destination_floor=destination_floor,
                    request_type="floor")

        except Elevator.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        return Response(status=status.HTTP_200_OK)

    @action(detail=True, methods=['POST'])
    def call_elevator(self, request, *args, **kwargs):
        try:
            requested_floor = int(request.POST.get('requested_floor'))
            if requested_floor:
                elevator = Elevator.objects.get(id=kwargs.get('pk'))
                ElevatorRequest.objects.create(
                    elevator=elevator, request_type="elevator")
                if elevator.running_status == "stop":
                    if elevator.current_floor == requested_floor:
                        elevator.door_status = "open"
                        return Response({"message": "Floor is same as current floor"},
                                        status=status.HTTP_400_BAD_REQUEST)
                    else:
                        elevator.running_status = "start"
                        if elevator.door_status == "close":
                            self.decide_direction(
                                requested_floor=requested_floor,
                                elevator=elevator)
                        else:
                            elevator.door_status = "open"
                            self.decide_direction(
                                requested_floor=requested_floor,
                                elevator=elevator)

                else:
                    self.update_elevator(direction=elevator.direction, destination_floor=requested_floor,
                                         elevator=elevator)
        except Elevator.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        return Response(status=status.HTTP_200_OK)

    @staticmethod
    def update_elevator(direction: str, destination_floor: int, elevator: Elevator):
        elevator.direction = direction
        elevator_destination = []
        elevator_destination = json.loads(elevator.destination_floor)
        if isinstance(elevator_destination, list):
            elevator_destination.append(destination_floor)
        else:
            elevator_destination = [destination_floor, ]
        elevator_destination = list(set(elevator_destination))
        elevator.destination_floor = json.dumps(elevator_destination)
        elevator.save()

    def decide_direction(self, requested_floor: int, elevator: Elevator):
        if elevator.current_floor < requested_floor:
            self.update_elevator(
                direction="UP", destination_floor=requested_floor,
                elevator=elevator)
        else:
            self.update_elevator(
                direction="DOWN", destination_floor=requested_floor,
                elevator=elevator)
