from django.contrib import admin
from .models import Genre, Language, AgeLimit, DirectorAndActor, Movie


# Register your models here.
@admin.register(Genre)
class GenreAdmin(admin.ModelAdmin):
    list_display = ("name",)


@admin.register(Language)
class LanguageAdmin(admin.ModelAdmin):
    list_display = ("name",)


@admin.register(AgeLimit)
class AgeLimitAdmin(admin.ModelAdmin):
    list_display = ("age_limit", "description")


@admin.register(DirectorAndActor)
class DirectorAndActorAdmin(admin.ModelAdmin):
    list_display = ("name", "gender", "birth_date")


@admin.register(Movie)
class MovieAdmin(admin.ModelAdmin):
    list_display = ("title", "release_date", "duration")
    filter_horizontal = ("language", "genre", "director_and_actor")
