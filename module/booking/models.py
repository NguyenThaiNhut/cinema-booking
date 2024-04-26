from django.db import models
from module.hall.models import SeatDetail
from module.screening.models import Screening

# Create your models here.
class Booking(models.Model):
    seat_detail = models.ForeignKey(SeatDetail, on_delete=models.CASCADE)
    screening = models.ForeignKey(Screening, on_delete=models.CASCADE)

    class Meta:
        unique_together = ("seat_detail", "screening")