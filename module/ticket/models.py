from django.db import models
from module.custom_user.models import CustomUser
from module.booking.models import Booking

# Create your models here.
class Ticket(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    booking = models.ForeignKey(Booking, on_delete=models.CASCADE)
    price = models.DecimalField(max_digits=10, decimal_places=2)