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


class UserSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    username = serializers.CharField(max_length=32)
    first_name = serializers.CharField(max_length=32)
    last_name = serializers.CharField(max_length=32)


class RegisterSerializer(serializers.Serializer):
    email = serializers.EmailField(
        required=True,
        validators=[UniqueValidator(queryset=User.objects.all())]
    )
    password = serializers.CharField(
        max_length=32,
        write_only=True,
        required=True,
        validators=[validate_password]
    )
    password2 = serializers.CharField(
        max_length=32,
        write_only=True,
        required=True
    )

    username = serializers.CharField(max_length=32)
    first_name = serializers.CharField(max_length=32, required=True)
    last_name = serializers.CharField(max_length=32, required=True)

    def validate(self, attrs):
        if attrs['password'] != attrs['password2']:
            raise serializers.ValidationError({"password": "Passwords didn't match"})

        return attrs

    def create(self, validated_data):
        user = User.objects.create(
            username=validated_data['username'],
            email=validated_data['email'],
            first_name=validated_data['first_name'],
            last_name=validated_data['last_name'],
        )

        user.set_password(validated_data['password'])
        user.save()

        return user
