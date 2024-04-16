from django.db import models


# Create your models here.
class Genre(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Language(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class AgeLimit(models.Model):
    age_limit = models.CharField(max_length=50)
    description = models.TextField()

    def __str__(self):
        return self.age_limit


class DirectorAndActor(models.Model):
    GENDER_CHOICES = (
        ("Nam", "Nam"),
        ("Nữ", "Nữ"),
    )

    ROLE_CHOICES = (
        ("Đạo diễn", "Đạo diễn"),
        ("Diễn viên", "Diễn viên"),
        ("Đạo diễn và diễn viên", "Đạo diễn và diễn viên"),
    )

    avatar = models.ImageField(upload_to="avatars/")
    name = models.CharField(max_length=100)
    gender = models.CharField(max_length=3, choices=GENDER_CHOICES)
    birth_date = models.DateField()
    role = models.CharField(max_length=30, choices=ROLE_CHOICES)
    description = models.TextField(blank=True)

    def __str__(self):
        return self.name


class Movie(models.Model):
    title = models.CharField(max_length=200)
    poster = models.ImageField(upload_to="uploads/%Y/%m")
    trailer = models.URLField(null=True, blank=True)
    release_date = models.DateField()
    content = models.TextField()
    duration = models.IntegerField()

    age_limit = models.ForeignKey(AgeLimit, on_delete=models.CASCADE)
    language = models.ManyToManyField(Language)
    genre = models.ManyToManyField(Genre)
    director_and_actor = models.ManyToManyField(DirectorAndActor)

    def __str__(self):
        return self.title
