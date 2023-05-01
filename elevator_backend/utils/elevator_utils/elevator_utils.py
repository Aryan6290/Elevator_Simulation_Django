from elevator_apis.models.Elevator import Elevator
from elevator_apis.models.ElevatorRequest import ElevatorRequest


def move_elevator(elevator_id, direction, target_floor):
    elevator = Elevator.objects.get(pk=elevator_id)
    elevator.direction = direction
    elevator.is_moving = True
    ElevatorRequest.objects.create(elevator_current_floor=elevator.current_floor, target_floor=target_floor,
                                   elevator_id=elevator)
    elevator.last_floor = elevator.current_floor
    elevator.current_floor = target_floor
    elevator.save()
    return True
