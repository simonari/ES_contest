from django.urls import path, include, re_path

from . import views

urlpatterns = [
    path('api/booking/', views.RoomListView.as_view()),
    path('api/booking/<int:pk>/', views.RoomDetailView.as_view({"get": "retrieve"})),
    path('api/booking/<int:pk>/book', views.RoomDetailView.as_view({"patch": "partial_update"})),
    path('api/booking/booked/', views.RoomBookedListView.as_view()),
    path('api/drf-auth/', include('rest_framework.urls')),
    path(r'api/auth/', include('djoser.urls')),
    re_path(r'^auth/', include('djoser.urls.authtoken')),
]
