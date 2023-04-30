from rest_framework import viewsets, status
from rest_framework.response import Response
from elevator_apis.models import Elevator
from django.core.cache import cache


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


