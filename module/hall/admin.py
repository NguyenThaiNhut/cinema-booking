from django.contrib import admin
from .models import Address, CinemaBrand, Cinema, HallType, Hall

# Register your models here.

@admin.register(Address)
class AddressAdmin(admin.ModelAdmin):
    list_display = ('province',)

@admin.register(CinemaBrand)
class CinemaBrandAdmin(admin.ModelAdmin):
    list_display = ('name', 'description')

@admin.register(Cinema)
class CinemaAdmin(admin.ModelAdmin):
    list_display = ('name', 'address', 'brand')

@admin.register(HallType)
class HallTypeAdmin(admin.ModelAdmin):
    list_display = ('name',)

@admin.register(Hall)
class HallAdmin(admin.ModelAdmin):
    list_display = ('hall_number', 'hall_type', 'seats_number', 'cinema')