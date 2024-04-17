from django.contrib import admin
from .models import Genre, Language, AgeLimit, DirectorAndActor, Movie


# Register your models here.
@admin.register(Genre)
class GenreAdmin(admin.ModelAdmin):
    list_display = ("id", "name",)


@admin.register(Language)
class LanguageAdmin(admin.ModelAdmin):
    list_display = ("id", "name",)


@admin.register(AgeLimit)
class AgeLimitAdmin(admin.ModelAdmin):
    list_display = ("id", "age_limit", "description")


@admin.register(DirectorAndActor)
class DirectorAndActorAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "gender", "birth_date")


@admin.register(Movie)
class MovieAdmin(admin.ModelAdmin):
    list_display = ("id", "title", "release_date", "duration")
    filter_horizontal = ("language", "genre", "director_and_actor")
