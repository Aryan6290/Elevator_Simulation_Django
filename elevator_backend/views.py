from django.db.models import F
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django.core.cache import cache

from elevator_apis.models.Elevator import Elevator
from elevator_apis.models.ElevatorRequest import ElevatorRequest
from elevator_apis.serializer import ElevatorSerializer
from elevator_backend.utils.elevator_utils.elevator_utils import move_elevator
from django.db.models.functions import Abs


class ElevatorSystemViewset(viewsets.ModelViewSet):
    queryset = Elevator.objects.all()
    serializer_class = ElevatorSerializer

    @action(detail=False, methods=['POST'], name='Initialise')
    def initialise(self, request):
        try:
            # Getting all the inputs for initialising elevator system

            number_of_lifts = request.data.get('lifts_count')
            max_floor = request.data.get("max_floor")
            min_floor = request.data.get("min_floor")
            lift_positions = request.data.get("lift_positions")
            # setting global variables in cache
            cache.set('max_floor', max_floor, timeout=None)
            cache.set('min_floor', min_floor, timeout=None)
            cache.set('number_of_lifts', number_of_lifts, timeout=None)

            new_elevators = []

            for i in range(0, number_of_lifts):
                # Creating elevator objects
                new_elevator = Elevator.objects.create(current_floor=lift_positions[i])
                new_elevators.append(new_elevator)

            return Response(status=status.HTTP_200_OK)
        except Exception as e:
            print(e)
            return Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    @action(detail=False, methods=['POST'], name='Patch')
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

    @action(detail=False, methods=['POST'], name='Call Elevator', url_path='call')
    def call_for_elevator(self, request):
        try:
            calls = request.data.get('calls')
            max_floor = cache.get('max_floor')
            min_floor = cache.get('min_floor')
            print(max_floor, min_floor)
            assigned_elevators = []
            for target_floor in calls:
                if target_floor < min_floor or target_floor > max_floor:
                    return Response(status=status.HTTP_400_BAD_REQUEST, exception="Floor is out of bounds!")
                # FCFS algorithm for getting the nearest elevator for each floor
                nearest_elevator = Elevator.objects.filter(
                    is_operational=True,
                    is_moving=False,
                ).annotate(
                    distance=Abs(F('current_floor') - target_floor)
                ).order_by('distance').first()
                if not nearest_elevator:
                    continue
                # -1 when lift is going down and +1 if it is going up
                direction = -1 if target_floor < nearest_elevator.current_floor else 1
                is_moving = move_elevator(nearest_elevator.id, direction, target_floor)
                assigned_elevators.append(nearest_elevator.id)
            # We set the lift to moving state so it is not selected again, hence resetting it here
            Elevator.objects.filter(is_moving=True).update(is_moving=False)
            return Response(status=status.HTTP_200_OK,
                            data={"assigned_elevators": assigned_elevators})
        except Exception as e:
            print(e)
            return Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR, exception=e)

    @action(detail=False, methods=['POST'], name='Elevator status', url_path='moving_status')
    def get_moving_status(self, request):
        try:
            elevator_id = request.data.get('elevator_id')
            elevator = Elevator.objects.get(pk=elevator_id)
            return Response(status=status.HTTP_200_OK, data={
                "direction": elevator.direction
            })
        except Elevator.DoesNotExist:
            return Response(status=status.HTTP_400_BAD_REQUEST, data={"message": "Elevator does not exists"})

    @action(detail=False, methods=['POST'], name='Destination Status', url_path='get_destination')
    def get_destination(self, request):
        try:
            elevator_id = request.data.get('elevator_id')
            elevator = Elevator.objects.get(pk=elevator_id)
            return Response(status=status.HTTP_200_OK, data={
                "destination": elevator.current_floor
            })
        except Elevator.DoesNotExist:
            return Response(status=status.HTTP_400_BAD_REQUEST, data={"message": "Elevator does not exists"})

    @action(detail=False, methods=['POST'], name='Destination Status',url_path='get_requests')
    def get_all_requests(self, request):
        try:
            elevator_id = request.data.get('elevator_id')
            elevator = Elevator.objects.get(pk=elevator_id)
            elevator_requests = ElevatorRequest.objects.filter(elevator_id=elevator)
            data = {'objects': list(elevator_requests.values())}
            return Response(status=status.HTTP_200_OK, data=data)
        except Elevator.DoesNotExist:
            return Response(status=status.HTTP_400_BAD_REQUEST, data={"message": "Elevator does not exists"})
