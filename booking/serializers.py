from rest_framework import serializers


class RoomSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    name = serializers.CharField(max_length=128)
    price = serializers.FloatField()
    beds = serializers.IntegerField()
    booked = serializers.BooleanField()
    available_from = serializers.DateTimeField()
