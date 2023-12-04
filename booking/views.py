from django.contrib.auth.models import User
from django.db.models import Q, QuerySet

from rest_framework import generics, viewsets, status
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from rest_framework.request import Request
from rest_framework.permissions import AllowAny, IsAuthenticated, BasePermission
from rest_framework.authentication import TokenAuthentication

from .models import Room
from .serializers import RoomSerializer, UserSerializer


class GetRoomInfoView(generics.ListAPIView):
    serializer_class = RoomSerializer
    permission_classes = [AllowAny, ]

    def _make_query(self) -> Q:
        params = self.request.query_params

        price_from = params.get('price_from')
        price_to = params.get('price_to')
        beds_from = params.get('beds_from')
        beds_to = params.get('beds_to')
        available_from_from = params.get('available_from')
        available_from_to = params.get('available_to')
        booked = True if "booked" in params.keys() else False
        vacant = True if "vacant" in params.keys() else False

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

        return query

    def get_queryset(self) -> QuerySet[Room]:
        query: Q = self._make_query()
        return Room.objects.filter(query)


class BookRoomView(viewsets.ModelViewSet):
    serializer_class = RoomSerializer
    authentication_classes = [TokenAuthentication, ]

    def get_permissions(self) -> list[BasePermission]:
        """Method to assign permissions to actions.\n
        - **retrieve** allowed to everyone\n
        - **partial_update** allowed only to authenticated users
        """
        permission_classes = [AllowAny]

        if self.action == "partial_update":
            permission_classes = [IsAuthenticated]

        return [permission() for permission in permission_classes]

    def get_queryset(self) -> Room:
        return Room.objects.get(pk=self.kwargs["pk"])

    def get_object(self) -> Room:
        return self.get_queryset()

    def partial_update(self, request: Request, *args, **kwargs) -> Response:
        room: Room = self.get_object()

        # If room not booked - book it by user
        if not room.booked:
            room.booked = True
            room.booked_by = request.user
            room.save()
            return Response("Room successfully booked", status=status.HTTP_200_OK)

        # If room is booked, we check that requesting user and user that has booked a room match
        # If it's not - server denies request
        if room.booked_by != request.user:
            return Response("You can't revert booking of this room", status=status.HTTP_401_UNAUTHORIZED)

        # Otherwise - booking will be reverted
        room.booked = False
        room.booked_by = None
        room.save()
        return Response("Booking successfully reverted!", status=status.HTTP_200_OK)


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
