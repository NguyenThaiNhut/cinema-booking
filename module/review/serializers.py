from rest_framework import serializers
from .models import (
    ReviewTag, Review
)

from module.movie.models import Movie
from module.custom_user.models import CustomUser

from module.movie.serializers import MovieSerializer
from module.custom_user.serializers import ProfileSerializer

class ReviewTagSerializer(serializers.ModelSerializer):
    class Meta:
        model = ReviewTag
        fields = ("id", "name")

    def validate_name(self, attrs):
        if ReviewTag.objects.filter(name=attrs):
            raise serializers.ValidationError("Review tag already exists.")
        return attrs
    
class ReviewSerializer(serializers.ModelSerializer):
    movie = MovieSerializer(read_only=True)
    customer = ProfileSerializer(read_only=True)
    tags = ReviewTagSerializer(many=True, read_only=True)

    movie_id = serializers.PrimaryKeyRelatedField(queryset=Movie.objects.all(), source='movie', write_only=True)
    customer_id = serializers.PrimaryKeyRelatedField(queryset=CustomUser.objects.all(), source='customer', write_only=True)
    tags_ids = serializers.PrimaryKeyRelatedField(queryset=ReviewTag.objects.all(), many=True, source='tags', write_only=True)

    def validate_star_rating(self, value):
        if value < 1 or value > 5:
            raise serializers.ValidationError("Star rating must be between 1 and 5.")
        return value

    class Meta:
        model = Review
        fields = (
            "id", 
            "movie", 
            "customer", 
            "star_rating", 
            "comment", 
            "like_count", 
            "tags", 
            "movie_id",
            "customer_id",
            "tags_ids", 
            "created_at",
        )
    
    def create(self, validated_data):
        movie_id = validated_data.get("movie").id
        customer_id = validated_data.get("customer").id
        tags_data = validated_data.pop("tags")

        review = Review.objects.create(**validated_data, movie_id=movie_id, customer_id=customer_id)

        review.tags.set(tags_data)
        return review
    
    def update(self, instance, validated_data):
        # Update fields of the Movie instance
        instance.star_rating = validated_data.get('star_rating', instance.star_rating)
        instance.comment = validated_data.get('comment', instance.comment)
    
        tags_data = validated_data.get('tags')
        if tags_data:
            instance.tags.set(tags_data)
        
        # Save the changes to the instance
        instance.save()
        return instance