from django.shortcuts import render
from django.db.models import Q
from rest_framework.response import Response
from rest_framework.request import Request
from rest_framework.views import APIView

from .models import Room
from .serializers import RoomSerializer


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
        serialized = RoomSerializer(queryset, many=True)
        return Response(serialized.data)
