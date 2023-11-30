from django.contrib import admin
from .models import Room

@admin.register(Room)
class RoomAdmin(admin.ModelAdmin):
    list_display = ("name", "price", "beds", "booked", "available_from",)
    list_filter = ("beds", "booked",)