from rest_framework import serializers
from .models import Booking

from module.hall.models import SeatDetail
from module.screening.models import Screening

from module.hall.serializers import SeatSerializer
from module.screening.serializers import ScreeningSerializer

class BookingSerializer(serializers.ModelSerializer):
    seat_detail = SeatSerializer(read_only=True)
    screening = ScreeningSerializer(read_only=True)

    seat_detail_id = serializers.PrimaryKeyRelatedField(queryset=SeatDetail.objects.all(), source='seat_detail', write_only=True)
    screening_id = serializers.PrimaryKeyRelatedField(queryset=Screening.objects.all(), source='screening', write_only=True)

    class Meta:
        model = Booking
        fields = (
            "id",
            "seat_detail",
            "screening",
            "seat_detail_id",
            "screening_id",
        )