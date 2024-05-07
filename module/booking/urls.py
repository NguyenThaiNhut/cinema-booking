from django.urls import path
from .views import (
    BookingAPIView 
)

urlpatterns = [
    path("booking/create-booking/", BookingAPIView.as_view(), name="create-booking")
]