from rest_framework import serializers
from .models import Hall, HallType, Cinema, CinemaBrand, Address

class AddressSerializer(serializers.ModelSerializer):
    class Meta:
        model = Address
        fields = ["id", "province"]

class CinemaBrandSerializer(serializers.ModelSerializer):
    class Meta:
        model = CinemaBrand
        fields = ["id", "name", "description"]

    def create(self, validated_data):
        cinema_id = validated_data.get("cinema").id
        hall_type_id = validated_data.get("hall_type").id

        movie = Hall.objects.create(**validated_data, cinema_id=cinema_id, hall_type_id=hall_type_id)
        return movie

class CinemaSerializer(serializers.ModelSerializer):
    address = AddressSerializer(read_only=True)
    brand = CinemaBrandSerializer(read_only=True)

    class Meta:
        model = Cinema
        fields = ["id", "name", "address", "brand"]

class HallTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = HallType
        fields = ["id", "name"]

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