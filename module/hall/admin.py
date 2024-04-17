from django.contrib import admin
from .models import Address, CinemaBrand, Cinema, HallType, Hall, SeatType, SeatDetail

# Register your models here.
@admin.register(Address)
class AddressAdmin(admin.ModelAdmin):
    list_display = ("id", "province",)

@admin.register(CinemaBrand)
class CinemaBrandAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "description")

@admin.register(Cinema)
class CinemaAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "address", "brand")

@admin.register(HallType)
class HallTypeAdmin(admin.ModelAdmin):
    list_display = ("id", "name",)

@admin.register(Hall)
class HallAdmin(admin.ModelAdmin):
    list_display = ("id", "hall_number", "hall_type", "seats_number", "cinema")

@admin.register(SeatType)
class SeatTypeAdmin(admin.ModelAdmin):
    list_display = ("id", "name",)

@admin.register(SeatDetail)
class SeatAdmin(admin.ModelAdmin):
    list_display = ("id", "hall", "seat_row", "seat_column", "seat_type")