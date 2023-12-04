from django.contrib.auth.models import User
from django.contrib.auth.password_validation import validate_password
from rest_framework import serializers
from rest_framework.validators import UniqueValidator


class RoomSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    number = serializers.IntegerField()
    name = serializers.CharField(max_length=128)
    price = serializers.FloatField()
    beds = serializers.IntegerField()
    booked = serializers.BooleanField()
    available_from = serializers.DateTimeField()
