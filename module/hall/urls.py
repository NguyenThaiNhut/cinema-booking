from django.urls import path

from .views import (
    GetListCinemaBrandAPIView, CinemaBrandAPIView,
    GetListCinemaAPIView, CinemaAPIView,
    GetListHallTypeAPIView, HallTypeAPIView,
    GetListHallAPIView, HallAPIView,
    GetListSeatTypeAPIView, SeatTypeAPIView,
    GetListSeatAPIView, SeatAPIView,
    GetListAddressAPIView, SearchAddressAPIView,
    GetListCienmaAPIView, SearchCinemaAPIView, FilterCinemaByBrandAPIView, GetDetailCienmaAPIView, UserFavoriteCinemaAPIView,
    SendEmailAPIView
)

urlpatterns = [
    # api of admin
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

    # api of customer
    path("address/get-list-address/", GetListAddressAPIView.as_view(), name="get-list-address"), 
    path("address/search/", SearchAddressAPIView.as_view(), name="search-address"), 

    path("cinema/get-list-cinema/<int:address_id>/", GetListCienmaAPIView.as_view(), name="get-list-cinema-by-address"), 
    path("cinema/search/", SearchCinemaAPIView.as_view(), name="search-cinema-by_address"), 
    path("cinema/filter/brand/", FilterCinemaByBrandAPIView.as_view(), name="filter-cinema-by-brand-by-address"),   
    path("cinema/detail/<int:cinema_id>/", GetDetailCienmaAPIView.as_view(), name="get-detail-cinema"),

    path("cinema/add-user-favorite-cinema/", UserFavoriteCinemaAPIView.as_view(), name="add-user-favorite-cinema"),
    path("cinema/delete-user-favorite-cinema/<int:user_favorite_cinema_id>", UserFavoriteCinemaAPIView.as_view(), name="delete-user-favorite-cinema"),
    path("cinema/get-list-user-favorite-cinema/", UserFavoriteCinemaAPIView.as_view(), name="get-list-user-favorite-cinema"),

    path("test-email/", SendEmailAPIView.as_view(), name="test-email"),
]