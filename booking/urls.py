from django.urls import path

from . import views

urlpatterns = [
    path('api/booking', views.GetRoomInfoView.as_view()),
    path('api/booking/<int:pk>', views.BookRoomView.as_view()),
    path('api/profile', views.UserDetailView.as_view()),
    path('api/profile/booked', views.BookedRoomListView.as_view()),
    path('api/register', views.UserRegisterView.as_view()),
    path('api/login', views.UserLogInView.as_view()),
    path('api/logout', views.UserLogOutView.as_view()),
]
