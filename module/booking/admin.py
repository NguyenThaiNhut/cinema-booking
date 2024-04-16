from django.contrib import admin
from .models import Booking

# Register your models here.
@admin.register(Booking)
class AddressAdmin(admin.ModelAdmin):
    list_display = ('seat_detail', 'screening')


