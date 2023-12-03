from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from django.db.models import Q, QuerySet

from rest_framework import generics, status
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from rest_framework.request import Request
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.authentication import TokenAuthentication

from .models import Room
from .serializers import RoomSerializer, UserSerializer, RegisterSerializer


class GetRoomInfoView(APIView):
    def get(self, request: Request):
        p = request.query_params

        price_from = p.get('price_from')
        price_to = p.get('price_to')
        beds_from = p.get('beds_from')
        beds_to = p.get('beds_to')
        available_from_from = p.get('available_from')
        available_from_to = p.get('available_to')
        booked = True if "booked" in p.keys() else False
        vacant = True if "vacant" in p.keys() else False

        query = Q()

        if price_from:
            query &= Q(price__gte=price_from)
        if price_to:
            query &= Q(price__lte=price_to)
        if beds_from:
            query &= Q(beds__gte=beds_from)
        if beds_to:
            query &= Q(beds__lte=beds_to)
        if available_from_from:
            query &= Q(available_from__gte=available_from_from)
        if available_from_to:
            query &= Q(available_from__lte=available_from_to)
        if booked ^ vacant:
            if booked:
                query &= Q(booked=True)
            else:
                query &= Q(booked=False)

        queryset = Room.objects.filter(query)
        serializer = RoomSerializer(queryset, many=True)
        return Response(serializer.data)


class BookRoomView(APIView):
    serializer_class = RoomSerializer
    authentication_classes = [TokenAuthentication, ]

    def get_permissions(self):
        permission_classes = [AllowAny(), ]

        if self.request.method == "PUT":
            permission_classes = [IsAuthenticated(), ]

        return permission_classes

    def get_queryset(self):
        return Room.objects.get(pk=self.kwargs['pk'])

    def put(self, request, *args, **kwargs):
        """Method to book a room or revert booking of room"""
        room = self.get_queryset()

        # TODO: there might be cleaner way to perform this operations
        if room.booked:
            if room.booked_by == request.user:
                room.booked = False
                room.booked_by = None
                room.save()
                return Response("Booking successfully reverted!", status=status.HTTP_200_OK)
            else:
                return Response("You can't revert booking of this room", status=status.HTTP_401_UNAUTHORIZED)
        else:
            room.booked = True
            room.booked_by = request.user
            room.save()
            return Response("Room successfully booked", status=status.HTTP_200_OK)

    def get(self, request, *args, **kwargs):
        room = self.get_queryset()
        serializer = RoomSerializer(room)
        return Response(serializer.data)


class BookedRoomListView(generics.ListAPIView):
    serializer_class = RoomSerializer
    authentication_classes = [TokenAuthentication, ]
    permission_classes = [IsAuthenticated, ]

    def get_queryset(self) -> QuerySet[Room]:
        user: User = self.request.user
        rooms: QuerySet[Room] = Room.objects.filter(booked_by=user)
        return rooms


class UserDetailView(generics.RetrieveAPIView):
    serializer_class = UserSerializer
    authentication_classes = [TokenAuthentication, ]
    permission_classes = [IsAuthenticated, ]

    def get_queryset(self) -> User:
        return Token.objects.get(key=self.request.user.auth_token).user

    def get_object(self) -> User:
        return self.get_queryset()


class UserRegisterView(generics.CreateAPIView):
    permission_classes = (AllowAny,)
    serializer_class = RegisterSerializer


class UserLogInView(APIView):
    permission_classes = (AllowAny,)

    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')

        user = None

        try:
            user = User.objects.get(username=username)
        except:
            pass

        if user is not None:
            user = authenticate(username=username, password=password)

        if user:
            token, _ = Token.objects.get_or_create(user=user)
            return Response({'token': token.key}, status=status.HTTP_200_OK)

        return Response({'error': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)


class UserLogOutView(APIView):
    permission_classes = [IsAuthenticated, ]

    def post(self, request):
        try:
            request.user.auth_token.delete()
            return Response({'message': 'Successfully logged out'}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
