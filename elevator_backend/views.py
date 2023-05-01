from django.db.models import F
from rest_framework import viewsets, status
from rest_framework.response import Response
from elevator_apis.models import Elevator
from django.core.cache import cache

from elevator_apis.serializer import ElevatorSerializer
from elevator_backend.utils.elevator_utils.elevator_utils import move_elevator


class ElevatorSystemAPI(viewsets.GenericViewSet):
    def initialise(self, request):
        try:
            number_of_lifts = request.data.get('lifts_count')
            max_floor = request.data.get("max_floor")
            min_floor = request.data.get("min_floor")
            lift_positions = request.data.get("lift_positions")
            cache.set('max_floor', max_floor, timeout=None)
            cache.set('min_floor', min_floor, timeout=None)
            cache.set('number_of_lifts', number_of_lifts, timeout=None)

            new_elevators = []

            for i in range(0, number_of_lifts):
                new_elevator = Elevator.objects.create(current_floor=lift_positions[i])
                new_elevators.append(new_elevator)

            return Response(status=status.HTTP_200_OK)
        except Exception as e:
            return Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR)

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

    def call_for_elevator(self, request):
        try:
            calls = request.data.get('calls')
            max_floor = cache.get('max_floor')
            min_floor = cache.get('min_floor')
            assigned_elevators = []
            for target_floor in calls:
                if target_floor < min_floor or target_floor > max_floor:
                    return Response(status=status.HTTP_400_BAD_REQUEST, exception="Floor is out of bounds!")

                nearest_elevator = Elevator.objects.filter(
                    is_operational=True,
                    is_moving=False,
                ).annotate(
                    distance=abs(F('current_floor') - target_floor)
                ).order_by('distance').first()
                direction = -1 if target_floor < nearest_elevator.current_floor else 1
                is_moving = move_elevator(nearest_elevator.id, direction)
                assigned_elevators.append(nearest_elevator.id)

            Elevator.objects.filter(is_moving=True).update(is_moving=False)
            return Response(status=status.HTTP_200_OK,
                            data={"assigned_elevators": assigned_elevators})
        except Exception as e:
            return Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR, exception=e)

    def get_moving_status(self, request):
        try:
            elevator_id = request.data.get('elevator_id')
            elevator = Elevator.objects.get(pk=elevator_id)
            return Response(status=status.HTTP_200_OK, data={
                "direction": elevator.direction
            })
        except Elevator.DoesNotExist:
            return Response(status=status.HTTP_400_BAD_REQUEST, data={"message": "Elevator does not exists"})

    def get_destination(self, request):
        try:
            elevator_id = request.data.get('elevator_id')
            elevator = Elevator.objects.get(pk=elevator_id)
            return Response(status=status.HTTP_200_OK, data={
                "direction": elevator.current_floor
            })
        except Elevator.DoesNotExist:
            return Response(status=status.HTTP_400_BAD_REQUEST, data={"message": "Elevator does not exists"})
