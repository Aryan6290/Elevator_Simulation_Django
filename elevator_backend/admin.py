from django.contrib import admin

from elevator_apis.models import Elevator, ElevatorRequest
from elevator_backend.views import ElevatorSystemViewset


admin.register('Elevator', Elevator)
admin.register('Request', ElevatorRequest)