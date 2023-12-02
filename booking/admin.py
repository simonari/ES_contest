from django.contrib import admin
from .models import Room


@admin.register(Room)
class RoomAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'price', 'beds', 'booked', 'available_from', 'booked_by', ]
    list_filter = ['beds', 'booked', ]
