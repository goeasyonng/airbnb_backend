from django.contrib import admin
from .models import Room, Amenity

@admin.register(Room)
class RoomAdmin(admin.ModelAdmin):
    list_display = ("name", "price", "kind", "total_amenities", "owner","created_at","updated_at",)
    list_filter = ("country","city","rooms","toilets","pet_friendly","kind","amenities","created_at","updated_at",)
    
    
    def total_amenities(self,room):
        return room.amenities.count()
    
@admin.register(Amenity)
class AmenityAdmin(admin.ModelAdmin):
    list_display = ("name","description","created_at","updated_at",)
    readonly_fields=("created_at", "updated_at",)