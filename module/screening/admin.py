from django.contrib import admin
from .models import Screening, ScreeningPrice

# Register your models here.
@admin.register(Screening)
class ScreeningAdmin(admin.ModelAdmin):
    list_display = ("id", "movie", "hall", "start_time", "remaining_seats", "price")
    list_filter = ("movie", "hall")
    search_fields = ("movie__title", "hall__name")

@admin.register(ScreeningPrice)
class ScreeningPriceAdmin(admin.ModelAdmin):
    list_display = ("id", "day_type", "description", "base_price")