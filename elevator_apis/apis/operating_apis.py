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
