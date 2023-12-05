"""DRF serializers"""
from rest_framework import serializers


class RoomSerializer(serializers.Serializer):
    """Serializer to `models.Room` model"""
    id = serializers.IntegerField(read_only=True)
    number = serializers.IntegerField()
    name = serializers.CharField(max_length=128)
    price = serializers.FloatField()
    beds = serializers.IntegerField()
    booked = serializers.BooleanField()
    available_from = serializers.DateTimeField()
