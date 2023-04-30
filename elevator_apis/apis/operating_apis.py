from django.core.cache import cache
from django.forms import models

from rest_framework import viewsets, status
from rest_framework.generics import get_object_or_404, GenericAPIView
from rest_framework.response import Response

from elevator_apis.models import Elevator
from elevator_apis.serializer import ElevatorSerializer


class ElevatorAPView(GenericAPIView):
    queryset = Elevator.objects.all()
    serializer_class = ElevatorSerializer

    def patch(self, request, pk):
        try:
            elevator = Elevator.objects.get(pk=pk)
        except Elevator.DoesNotExist:
            return Response(status=status.HTTP_400_BAD_REQUEST, data={"message": "Elevator does not exists"})
        if 'is_operational' in request.data:
            elevator.is_operational = not request.data['is_operational']
        if 'door_opened' in request.data:
            elevator.door_opened = request.data['door_opened']
        elevator.save()
        serializer = ElevatorSerializer(elevator)
        return Response(serializer.data, status=status.HTTP_200_OK)

    # def move_elevator(self, request):
    #     elevator_id = request.data.get('elevator_id')
    #     try:
    #         elevator = Elevator.objects.get(pk=elevator_id)
    #         elevator.current_floor =
    #
    #     except Elevator.DoesNotExist:
    #         return Response(status=status.HTTP_400_BAD_REQUEST, data={"message": "Elevator does not exists"})
    #     except Exception as e:
    #         return Response(status = status.HTTP_500_INTERNAL_SERVER_ERROR)
