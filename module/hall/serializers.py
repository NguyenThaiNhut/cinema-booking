from rest_framework import serializers
from .models import (
    Address, 
    CinemaBrand, Cinema, 
    HallType, Hall,
    SeatType, SeatDetail
)
from module.custom_user.models import CustomUser, UserFavoriteCinema
from module.custom_user.serializers import ProfileSerializer


class AddressSerializer(serializers.ModelSerializer):
    class Meta:
        model = Address
        fields = ["id", "province"]


class CinemaBrandSerializer(serializers.ModelSerializer):
    class Meta:
        model = CinemaBrand
        fields = ["id", "name", "description"]

    def validate_name(self, attrs):
        if CinemaBrand.objects.filter(name=attrs):
            raise serializers.ValidationError("Cinema brand already exists.")
        return attrs
    

class CinemaSerializer(serializers.ModelSerializer):
    address = AddressSerializer(read_only=True)
    brand = CinemaBrandSerializer(read_only=True)

    address_id = serializers.PrimaryKeyRelatedField(queryset=Address.objects.all(), source='address', write_only=True)
    brand_id = serializers.PrimaryKeyRelatedField(queryset=CinemaBrand.objects.all(), source='brand', write_only=True)

    class Meta:
        model = Cinema
        fields = ["id", "name", "address", "brand", "address_id", "brand_id"]

    def create(self, validated_data):
        address_id = validated_data.get("address").id
        brand_id = validated_data.get("brand").id

        movie = Cinema.objects.create(**validated_data, address_id=address_id, brand_id=brand_id)
        return movie

    def update(self, instance, validated_data):
        instance.name = validated_data.get('name', instance.name)
        instance.address = validated_data.get('address', instance.address)
        instance.brand = validated_data.get('brand', instance.brand)

        instance.save()
        return instance
    

class UserFavoriteCinemaSerializer(serializers.ModelSerializer):
    user = ProfileSerializer(read_only=True)
    cinema = CinemaSerializer(read_only=True)

    user_id = serializers.PrimaryKeyRelatedField(queryset=CustomUser.objects.all(), source='user', write_only=True)
    cinema_id = serializers.PrimaryKeyRelatedField(queryset=Cinema.objects.all(), source='cinema', write_only=True)

    class Meta:
        model = UserFavoriteCinema
        fields = ["id", "user", "cinema", "user_id", "cinema_id"]

    def create(self, validated_data):
        user_id = validated_data.get("user").id
        cinema_id = validated_data.get("cinema").id

        user_favorite_cinema = UserFavoriteCinema.objects.create(**validated_data, user_id=user_id, cinema_id=cinema_id)
        return user_favorite_cinema
    

class HallTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = HallType
        fields = ["id", "name"]

    def validate_name(self, attrs):
        if HallType.objects.filter(name=attrs):
            raise serializers.ValidationError("Hall type already exists.")
        return attrs


class HallSerializer(serializers.ModelSerializer):
    cinema = CinemaSerializer(read_only=True)
    hall_type = HallTypeSerializer(read_only=True)

    cinema_id = serializers.PrimaryKeyRelatedField(queryset=Cinema.objects.all(), source='cinema', write_only=True)
    hall_type_id = serializers.PrimaryKeyRelatedField(queryset=HallType.objects.all(), source='hall_type', write_only=True)

    class Meta:
        model = Hall
        fields = (
            "id",
            "hall_number",
            "seats_number",
            "cinema",
            "hall_type",
            "cinema_id",
            "hall_type_id",
        )

    def create(self, validated_data):
        cinema_id = validated_data.get("cinema").id
        hall_type_id = validated_data.get("hall_type").id

        movie = Hall.objects.create(**validated_data, cinema_id=cinema_id, hall_type_id=hall_type_id)
        return movie
    
    def update(self, instance, validated_data):
        instance.hall_number = validated_data.get('hall_number', instance.hall_number)
        instance.hall_type = validated_data.get('hall_type', instance.hall_type)
        instance.seats_number = validated_data.get('seats_number', instance.seats_number)
        instance.cinema = validated_data.get('cinema', instance.cinema)

        instance.save()
        return instance
    

class SeatTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = SeatType
        fields = ["id", "name"]

    def validate_name(self, attrs):
        if SeatType.objects.filter(name=attrs):
            raise serializers.ValidationError("Seat type already exists.")
        return attrs


class SeatSerializer(serializers.ModelSerializer):
    hall = HallSerializer(read_only=True)
    seat_type = SeatTypeSerializer(read_only=True)

    hall_id = serializers.PrimaryKeyRelatedField(queryset=Hall.objects.all(), source='hall', write_only=True)
    seat_type_id = serializers.PrimaryKeyRelatedField(queryset=SeatType.objects.all(), source='seat_type', write_only=True)

    class Meta:
        model = SeatDetail
        fields = (
            "id",
            "hall",
            "seat_row",
            "seat_column",
            "seat_type",
            "hall_id",
            "seat_type_id",
        )

    def create(self, validated_data):
        hall_id = validated_data.get("hall").id
        seat_type_id = validated_data.get("seat_type").id

        seat = SeatDetail.objects.create(**validated_data, hall_id=hall_id, seat_type_id=seat_type_id)
        return seat
    
    def update(self, instance, validated_data):
        instance.hall = validated_data.get('hall', instance.hall)
        instance.seat_row = validated_data.get('seat_row', instance.seat_row)
        instance.seat_column = validated_data.get('seat_column', instance.seat_column)
        instance.seat_type = validated_data.get('seat_type', instance.seat_type)

        instance.save()
        return instance
    
    