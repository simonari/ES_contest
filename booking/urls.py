from django.urls import path

from . import views

urlpatterns = [
    path('api/booking', views.GetRoomInfoView.as_view()),
    path('api/booking/<int:pk>', views.BookRoomView.as_view())
]
