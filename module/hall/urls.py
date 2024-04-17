from django.urls import path

from .views import (
    GetListCinemaBrandAPIView, CinemaBrandAPIView,
    GetListCinemaAPIView, CinemaAPIView,
    GetListHallTypeAPIView, HallTypeAPIView,
    GetListHallAPIView, HallAPIView,
    GetListSeatTypeAPIView, SeatTypeAPIView,
    GetListSeatAPIView, SeatAPIView,
)

urlpatterns = [
    path("admin-user/cinema-brand/get-brand-by-id/<str:brand_id>/", GetListCinemaBrandAPIView.as_view(), name="get-brand-by-id"), 
    path("admin-user/cinema-brand/add-brand/", CinemaBrandAPIView.as_view(), name="add-brand"),
    path("admin-user/cinema-brand/update-brand/<int:brand_id>/", CinemaBrandAPIView.as_view(), name="update-brand"),
    path("admin-user/cinema-brand/delete-brand/<int:brand_id>/", CinemaBrandAPIView.as_view(), name="delete-brand"),

    path("admin-user/cinema/get-cinema-by-id/<str:cinema_id>/", GetListCinemaAPIView.as_view(), name="get-cinema-by-id"), 
    path("admin-user/cinema/add-cinema/", CinemaAPIView.as_view(), name="add-cinema"),
    path("admin-user/cinema/update-cinema/<int:cinema_id>/", CinemaAPIView.as_view(), name="update-cinema"),
    path("admin-user/cinema/delete-cinema/<int:cinema_id>/", CinemaAPIView.as_view(), name="delete-cinema"),

    path("admin-user/hall-type/get-type-by-id/<str:type_id>/", GetListHallTypeAPIView.as_view(), name="get-hall-type-by-id"), 
    path("admin-user/hall-type/add-type/", HallTypeAPIView.as_view(), name="add-hall-type"),
    path("admin-user/hall-type/update-type/<int:type_id>/", HallTypeAPIView.as_view(), name="update-hall-type"),
    path("admin-user/hall-type/delete-type/<int:type_id>/", HallTypeAPIView.as_view(), name="delete-hall-type"),

    path("admin-user/hall/get-hall-by-id/<str:hall_id>/", GetListHallAPIView.as_view(), name="get-hall-by-id"), 
    path("admin-user/hall/add-hall/", HallAPIView.as_view(), name="add-hall"),
    path("admin-user/hall/update-hall/<int:hall_id>/", HallAPIView.as_view(), name="update-hall"),
    path("admin-user/hall/delete-hall/<int:hall_id>/", HallAPIView.as_view(), name="delete-hall"),

    path("admin-user/seat-type/get-type-by-id/<str:type_id>/", GetListSeatTypeAPIView.as_view(), name="get-seat-type-by-id"), 
    path("admin-user/seat-type/add-type/", SeatTypeAPIView.as_view(), name="add-seat-type"),
    path("admin-user/seat-type/update-type/<int:type_id>/", SeatTypeAPIView.as_view(), name="update-seat-type"),
    path("admin-user/seat-type/delete-type/<int:type_id>/", SeatTypeAPIView.as_view(), name="delete-seat-type"),

    path("admin-user/seat/get-seat-by-id/<str:seat_id>/", GetListSeatAPIView.as_view(), name="get-seat-by-id"), 
    path("admin-user/seat/add-seat/", SeatAPIView.as_view(), name="add-seat"),
    path("admin-user/seat/update-seat/<int:seat_id>/", SeatAPIView.as_view(), name="update-seat"),
    path("admin-user/seat/delete-seat/<int:seat_id>/", SeatAPIView.as_view(), name="delete-seat"),
]