from rest_framework import serializers
from .models import ScreeningPrice, Screening

from module.movie.models import Movie
from module.hall.models import Hall

from module.movie.serializers import MovieSerializer
from module.hall.serializers import HallSerializer


class ScreeningPriceSerializer(serializers.ModelSerializer):
    class Meta:
        model = ScreeningPrice
        fields = '__all__'

    def validate_day_type(self, attrs):
        if ScreeningPrice.objects.filter(day_type=attrs):
            raise serializers.ValidationError("Screening Price already exists.")
        return attrs
    

class ScreeningSerializer(serializers.ModelSerializer):
    movie = MovieSerializer(read_only=True)
    hall = HallSerializer(read_only=True)
    price = ScreeningPriceSerializer(read_only=True)

    movie_id = serializers.PrimaryKeyRelatedField(queryset=Movie.objects.all(), source='movie', write_only=True)
    hall_id = serializers.PrimaryKeyRelatedField(queryset=Hall.objects.all(), source='hall', write_only=True)
    price_id = serializers.PrimaryKeyRelatedField(queryset=ScreeningPrice.objects.all(), source='price', write_only=True)

    class Meta:
        model = Screening
        fields = ["id", "movie", "hall", "start_time", "remaining_seats", "price", "movie_id", "hall_id", "price_id"]

    def create(self, validated_data):
        movie_id = validated_data.get("movie").id
        hall_id = validated_data.get("hall").id
        price_id = validated_data.get("price").id

        movie = Screening.objects.create(**validated_data, movie_id=movie_id, hall_id=hall_id, price_id=price_id)
        return movie

    def update(self, instance, validated_data):
        instance.movie = validated_data.get('movie', instance.movie)
        instance.hall = validated_data.get('hall', instance.hall)
        instance.start_time = validated_data.get('brand', instance.start_time)
        instance.remaining_seats = validated_data.get('remaining_seats', instance.remaining_seats)
        instance.price = validated_data.get('price', instance.price)

        instance.save()
        return instance

    


    