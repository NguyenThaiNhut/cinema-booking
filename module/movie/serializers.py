from rest_framework import serializers
from .models import Movie, Genre, Language, AgeLimit, DirectorAndActor

class AgeLimitSerializer(serializers.ModelSerializer):
    class Meta:
        model = AgeLimit
        fields = ["id", "age_limit", "description"]

class GenreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Genre
        fields = ["id", "name"]

class LanguageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Language
        fields = ["id", "name"]

class DirectorAndActorSerializer(serializers.ModelSerializer):
    class Meta:
        model = DirectorAndActor
        fields = ["id", "avatar", "name", "gender", "birth_date", "role", "description"]

class MovieSerializer(serializers.ModelSerializer):
    age_limit = AgeLimitSerializer(read_only=True)
    language = LanguageSerializer(many=True, read_only=True)
    genre = GenreSerializer(many=True, read_only=True)
    director_and_actor = DirectorAndActorSerializer(many=True, read_only=True)

    age_limit_id = serializers.PrimaryKeyRelatedField(queryset=AgeLimit.objects.all(), source='age_limit', write_only=True)
    language_ids = serializers.PrimaryKeyRelatedField(queryset=Language.objects.all(), many=True, source='language', write_only=True)
    genre_ids = serializers.PrimaryKeyRelatedField(queryset=Genre.objects.all(), many=True, source='genre', write_only=True)
    director_and_actor_ids = serializers.PrimaryKeyRelatedField(queryset=DirectorAndActor.objects.all(), many=True, source='director_and_actor', write_only=True)

    num_bookings = serializers.IntegerField(required=False) # optional field

    class Meta:
        model = Movie
        fields = (
            "id",
            "title",
            "poster",
            "poster_name",
            "trailer",
            "release_date",
            "content",
            "duration",
            "age_limit",
            "language",
            "genre",
            "director_and_actor",
            "age_limit_id",
            "language_ids", 
            "genre_ids", 
            "director_and_actor_ids",
            "num_bookings",
        )

    def create(self, validated_data):
        age_limit_id = validated_data.get("age_limit").id
        language_data = validated_data.pop("language")
        genre_data = validated_data.pop("genre")
        director_and_actor_data = validated_data.pop("director_and_actor")

        movie = Movie.objects.create(**validated_data, age_limit_id=age_limit_id)

        movie.language.set(language_data)
        movie.genre.set(genre_data)
        movie.director_and_actor.set(director_and_actor_data)
        return movie

    def update(self, instance, validated_data):
        # Update fields of the Movie instance
        instance.title = validated_data.get('title', instance.title)
        instance.poster = validated_data.get('poster', instance.poster)
        instance.poster_name = validated_data.get('poster_name', instance.poster_name)
        instance.trailer = validated_data.get('trailer', instance.trailer)
        instance.release_date = validated_data.get('release_date', instance.release_date)
        instance.content = validated_data.get('content', instance.content)
        instance.duration = validated_data.get('duration', instance.duration)
        
        # Update age limit
        age_limit_data = validated_data.get('age_limit')
        if age_limit_data: 
            instance.age_limit = age_limit_data
        
        # Update languages
        language_data = validated_data.get('language')
        if language_data:
            instance.language.set(language_data)
        
        # Update genres
        genre_data = validated_data.get('genre')
        if genre_data:
            instance.genre.set(genre_data)
        
        # Update directors and actors
        director_and_actor_data = validated_data.get('director_and_actor')
        if director_and_actor_data:
            instance.director_and_actor.set(director_and_actor_data)
        
        # Save the changes to the instance
        instance.save()
        return instance