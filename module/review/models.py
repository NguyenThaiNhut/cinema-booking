from django.db import models
from module.movie.models import Movie
from module.custom_user.models import CustomUser

# Create your models here.
class ReviewTag(models.Model):
    name = models.CharField(max_length=50)

class Review(models.Model):
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE)
    customer = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    star_rating = models.IntegerField()
    comment = models.TextField()
    like_count = models.IntegerField(default=0)
    tags = models.ManyToManyField(ReviewTag)