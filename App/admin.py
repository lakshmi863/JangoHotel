from django.contrib import admin
from .models import Hotel_details

class HotelDetailsAdmin(admin.ModelAdmin):
    list_display = ('name', 'rating', 'price', 'room_type')  # Customize columns shown

admin.site.register(Hotel_details, HotelDetailsAdmin)