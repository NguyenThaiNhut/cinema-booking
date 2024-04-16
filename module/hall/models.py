from django.db import models

# Create your models here.
class Address(models.Model):
    province = models.CharField(max_length=100)

    def __str__(self):
        return self.province

class CinemaBrand(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()

    def __str__(self):
        return self.name
    
class Cinema(models.Model):
    name = models.CharField(max_length=100)
    address = models.ForeignKey(Address, on_delete=models.CASCADE)
    brand = models.ForeignKey(CinemaBrand, on_delete=models.CASCADE)

    def __str__(self):
        return self.name

class HallType(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class Hall(models.Model):
    hall_number = models.IntegerField()
    hall_type = models.ForeignKey(HallType, on_delete=models.CASCADE)
    seats_number = models.IntegerField()
    cinema = models.ForeignKey(Cinema, on_delete=models.CASCADE)

    def __str__(self):
        return f"Hall {self.hall_number} - {self.cinema}"
    
class SeatType(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name
    
class SeatDetail(models.Model):
    hall = models.ForeignKey(Hall, on_delete=models.CASCADE)
    seat_row = models.IntegerField()
    seats_column = models.IntegerField()
    seat_type = models.ForeignKey(SeatType, on_delete=models.CASCADE)

    def __str__(self):
        return f"Seat detail: {self.hall} - {self.seat_type} - {self.seat_row}:{self.seats_column}"

