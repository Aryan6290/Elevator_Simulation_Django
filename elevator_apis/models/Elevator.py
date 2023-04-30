from django.db import models


class Elevator(models.Model):
    id = models.AutoField(primary_key=True)
    current_floor = models.PositiveIntegerField(null=False, blank=False)
    is_operational = models.BooleanField(default=True, null=False, blank=False)
    is_selected = models.BooleanField(default=True, null=False, blank=False)
    is_moving = models.BooleanField(default=True, null=False, blank=False)
    direction = models.IntegerField(null=False, blank=False, choices=[1, -1])
    door_opened = models.BooleanField(null=False, blank=False, default=False)
