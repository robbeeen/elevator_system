from django.shortcuts import render
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from elevators.models import Elevator


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

