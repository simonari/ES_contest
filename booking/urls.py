"""Endpoints list"""
from django.urls import path, include, re_path
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView

from . import views

urlpatterns = [
    path('api/booking/', views.RoomListView.as_view(), name='booking'),
    path('api/booking/<int:pk>/',
         views.RoomDetailView.as_view({"get": "retrieve"}),
         name='booking-room'),
    path('api/booking/<int:pk>/book',
         views.RoomDetailView.as_view({"patch": "partial_update"}),
         name='booking-room-book'),
    path('api/booking/booked/', views.RoomBookedListView.as_view(), name='booking-booked'),
    path('api/drf-auth/', include('rest_framework.urls')),
    path(r'api/auth/', include('djoser.urls')),
    re_path(r'^auth/', include('djoser.urls.authtoken')),
    path('api/schema/', SpectacularAPIView.as_view(), name='schema'),
    path('api/docs/', SpectacularSwaggerView.as_view(url_name='schema'))
]
