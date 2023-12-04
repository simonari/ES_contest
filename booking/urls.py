from django.urls import path, include, re_path

from . import views

urlpatterns = [
    path('api/booking/', views.GetRoomInfoView.as_view()),
    path('api/booking/<int:pk>/', views.BookRoomView.as_view({"get": "retrieve"})),
    path('api/booking/<int:pk>/book', views.BookRoomView.as_view({"patch": "partial_update"})),
    path('api/profile/booked/', views.BookedRoomListView.as_view()),
    path('api/profile', views.UserDetailView.as_view()),
    path('api/drf-auth/', include('rest_framework.urls')),
    path(r'api/auth/', include('djoser.urls')),
    re_path(r'^auth/', include('djoser.urls.authtoken')),
]
