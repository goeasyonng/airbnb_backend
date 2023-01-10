from django.contrib import admin
from .models import Room, Amenity

@admin.register(Room)
class RoomAdmin(admin.ModelAdmin):
    list_display = ("name", "price", "kind", "owner",)
    list_filter = ("country","city","rooms","toilets","pet_friendly","kind","amenities",)
@admin.register(Amenity)
class AmenityAdmin(admin.ModelAdmin):
    pass