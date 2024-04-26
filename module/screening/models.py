from django.db import models
from module.movie.models import Movie
from module.hall.models import Hall

# Create your models here.
class ScreeningPrice(models.Model):
    DAY_TYPE_CHOICES = [
        ('Regular', 'Regular'),
        ('Holiday', 'Holiday'),
    ]

    day_type = models.CharField(max_length=10, choices=DAY_TYPE_CHOICES, default=None)
    description = models.CharField(max_length=100)
    base_price = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"{self.day_type} - {self.base_price}"


class Screening(models.Model):
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE)
    hall = models.ForeignKey(Hall, on_delete=models.CASCADE)
    start_time = models.DateTimeField()
    remaining_seats = models.IntegerField()
    price = models.ForeignKey(ScreeningPrice, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.movie} - {self.hall} - {self.start_time} - {self.price}"

    