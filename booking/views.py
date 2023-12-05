"""Views file"""
from django.contrib.auth.models import User
from django.db.models import Q, QuerySet
from django.http import QueryDict

from rest_framework import generics, viewsets, status
from rest_framework.response import Response
from rest_framework.request import Request
from rest_framework.permissions import AllowAny, IsAuthenticated, BasePermission
from rest_framework.authentication import TokenAuthentication

from drf_spectacular.utils import (extend_schema, extend_schema_view,
                                   OpenApiParameter, OpenApiExample)

from .models import Room
from .serializers import RoomSerializer


@extend_schema(tags=['Booking'])
@extend_schema_view(
    get=extend_schema(
        summary='View to get list of rooms',
        description='Endpoint to get list of all rooms.\nParameters might be used to filter them.',
        parameters=[
            OpenApiParameter(
                name='price_from',
                location=OpenApiParameter.QUERY,
                description='Minimum price of the room',
                required=False
            ),
            OpenApiParameter(
                name='price_to',
                location=OpenApiParameter.QUERY,
                description='Maximum price of the room',
                required=False
            ),
            OpenApiParameter(
                name='beds_from',
                location=OpenApiParameter.QUERY,
                description='Minimum number of beds in room',
                required=False
            ),
            OpenApiParameter(
                name='beds_to',
                location=OpenApiParameter.QUERY,
                description='Maximum number of beds in room',
                required=False
            ),
            OpenApiParameter(
                name='available_from',
                location=OpenApiParameter.QUERY,
                description='Minimum datetime that room available from',
                required=False
            ),
            OpenApiParameter(
                name='available_to',
                location=OpenApiParameter.QUERY,
                description='Maximum datetime that room available from',
                required=False
            ),
            OpenApiParameter(
                name='booked',
                location=OpenApiParameter.QUERY,
                description='Filter to show already booked rooms',
                required=False,
            ),
            OpenApiParameter(
                name='vacant',
                location=OpenApiParameter.QUERY,
                description='Filter to show vacant rooms',
                required=False,
            ),
        ]
    )
)
class RoomListView(generics.ListAPIView):
    """View to get list of rooms"""
    serializer_class = RoomSerializer
    permission_classes = [AllowAny]

    def _make_query(self) -> Q:
        """Method to parse query params and make a DB-query"""
        params: QueryDict = self.request.query_params

        price_from: str = params.get(key='price_from')
        price_to: str = params.get(key='price_to')
        beds_from: str = params.get(key='beds_from')
        beds_to: str = params.get(key='beds_to')
        available_from_from: str = params.get(key='available_from')
        available_from_to: str = params.get(key='available_to')
        booked: bool = "booked" in params.keys()
        vacant: bool = "vacant" in params.keys()

        query: Q = Q()

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
        """Method to get query set containing room instances"""
        query: Q = self._make_query()
        return Room.objects.filter(query)


@extend_schema(tags=['Booking'])
@extend_schema_view(
    retrieve=extend_schema(
        summary='Get detailed info of room',
        description='Get detailed info about room to any user',
        parameters=[
            OpenApiParameter(
                name="id",
                location=OpenApiParameter.PATH,
                description="ID of room in database",
                required=True,
                type=int
            )
        ]
    ),
    partial_update=extend_schema(
        summary='Book room by user',
        description='Book available room by user or revert booking '
                    'if requesting user matches user that has booked a room',
        parameters=[
            OpenApiParameter(
                name="id",
                location=OpenApiParameter.PATH,
                description="ID of room in database",
                required=True,
                type=int
            ),
            OpenApiParameter(
                name="Authorization",
                location=OpenApiParameter.HEADER,
                description="Authorization token",
                required=True,
                type=str,
                examples=[
                    OpenApiExample("Token d8c719cea96554df7b4289f86d7f37c7c5faef20"),
                    OpenApiExample("Token 36e4ef60d3300e82595749c324d1fffb8db93b7d"),
                ]
            ),
        ]
    )
)
class RoomDetailView(viewsets.ModelViewSet):
    """A set of view for detailed info about specific room.\n
    - **retrieve** action responsible for getting single room instance;
    - **partial_update** action responsible for booking selected room;
    """
    serializer_class = RoomSerializer
    authentication_classes = [TokenAuthentication]

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
        """Method to get queryset containing room instance"""
        return Room.objects.get(pk=self.kwargs["pk"])

    def get_object(self) -> Room:
        """Method to get room instance """
        return self.get_queryset()

    def partial_update(self, request: Request, *args, **kwargs) -> Response:
        """Method that handling **PATCH** HTTP method.\n
        Responsible for booking room by user or reverting booking."""
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


@extend_schema(tags=['Booking'])
@extend_schema_view(
    get=extend_schema(
        summary='Get a list of booked by user rooms',
        description='Get a list of booked by user rooms',
        parameters=[
            OpenApiParameter(
                name="Authorization",
                location=OpenApiParameter.HEADER,
                description="Authorization token",
                required=True,
                type=str,
                examples=[
                    OpenApiExample("Token d8c719cea96554df7b4289f86d7f37c7c5faef20"),
                    OpenApiExample("Token 36e4ef60d3300e82595749c324d1fffb8db93b7d"),
                ]
            )],
    )
)
class RoomBookedListView(generics.ListAPIView):
    """View to get a list of booked by user rooms."""
    serializer_class = RoomSerializer
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get_queryset(self) -> QuerySet[Room]:
        """Method to get query set of rooms booked by user"""
        user: User = self.request.user
        rooms: QuerySet[Room] = Room.objects.filter(booked_by=user)
        return rooms