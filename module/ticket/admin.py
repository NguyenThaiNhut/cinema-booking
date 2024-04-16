from django.contrib import admin
from .models import Ticket

# Register your models here.
@admin.register(Ticket)
class TicketAdmin(admin.ModelAdmin):
    list_display = ('user', 'booking', 'price')
    list_filter = ('user',)
    search_fields = ('user__username',)
