from elevator_apis.models import Elevator


def move_elevator(elevator_id, direction, target_floor):
    elevator = Elevator.objects.get(pk=elevator_id)
    elevator.direction = direction
    elevator.is_moving = True
    elevator.last_floor = elevator.current_floor
    elevator.current_floor = target_floor
    elevator.save()
    return True
