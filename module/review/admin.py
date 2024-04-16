from django.contrib import admin
from .models import Review, ReviewTag

# Register your models here.
@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ('movie', 'customer', 'star_rating', 'comment', 'like_count')
    filter_horizontal = ('tags',)

@admin.register(ReviewTag)
class ReviewTagAdmin(admin.ModelAdmin):
    list_display = ('name',)