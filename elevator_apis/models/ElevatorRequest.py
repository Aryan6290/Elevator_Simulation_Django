from django.db import models


class ElevatorRequest(models.Model):
    id = models.AutoField(primary_key=True)
    elevator_current_floor = models.IntegerField(null=True, blank=False)
    target_floor = models.IntegerField(null=True, blank=False)
    request_time = models.DateTimeField(auto_now_add=True)
    elevator_id = models.ForeignKey('Elevator', related_name="elevator", on_delete=models.CASCADE,
                                    null=False, blank=False, )
