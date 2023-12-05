"""Django Models"""
from django.db import models
from django.contrib.auth.models import User


class Room(models.Model):
    """Model of single room"""
    id = models.AutoField(primary_key=True)
    number = models.PositiveIntegerField()
    name = models.CharField(max_length=128)
    price = models.FloatField()
    beds = models.PositiveIntegerField()
    booked = models.BooleanField(default=False)
    available_from = models.DateTimeField()
    booked_by = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True)
