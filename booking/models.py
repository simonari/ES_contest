from django.db import models


class Room(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=128)
    price = models.FloatField()
    beds = models.PositiveIntegerField()
    booked = models.BooleanField(default=False)
    available_from = models.DateTimeField()

