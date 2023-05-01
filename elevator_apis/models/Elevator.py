from django.db import models


class Elevator(models.Model):
    id = models.AutoField(primary_key=True)
    current_floor = models.IntegerField(null=False, blank=False, default=0)
    is_operational = models.BooleanField(default=True, null=False, blank=False)
    is_moving = models.BooleanField(default=False, null=False, blank=False)
    direction = models.IntegerField(null=True, blank=False)
    door_opened = models.BooleanField(null=False, blank=False, default=False)
    last_floor = models.IntegerField(null=True, blank=False)
