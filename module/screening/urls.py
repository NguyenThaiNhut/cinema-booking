from django.urls import path
from .views import (
    GetListScreeningPriceAPIView, ScreeningPriceAPIView,
    GetListScreeningAPIView, ScreeningAPIView,
    ScreeningByHallAPIView, GetScreeningDetailAPIView, 
)

urlpatterns = [
    path("admin-user/screening-price/get-price-by-id/<str:price_id>/", GetListScreeningPriceAPIView.as_view(), name="get-screening-price-by-id"),
    path("admin-user/screening-price/add-price/", ScreeningPriceAPIView.as_view(), name="add-screening-price"),
    path("admin-user/screening-price/update-price/<int:price_id>/", ScreeningPriceAPIView.as_view(), name="update-screening-price"),
    path("admin-user/screening-price/delete-price/<int:price_id>/", ScreeningPriceAPIView.as_view(), name="delete-screening-price"),
    
    path("admin-user/screening/get-screening-by-id/<str:screening_id>/", GetListScreeningAPIView.as_view(), name="get-screening-by-id"),
    path("admin-user/screening/add-screening/", ScreeningAPIView.as_view(), name="add-screening"),
    path("admin-user/screening/update-screening/<int:screening_id>/", ScreeningAPIView.as_view(), name="update-screening"),
    path("admin-user/screening/delete-screening/<int:screening_id>/", ScreeningAPIView.as_view(), name="delete-screening"),

    path("screening/get-screening-by-hall/<int:hall_id>/", ScreeningByHallAPIView.as_view(), name="get-screening-by-hall"),
    path("screening/get-screening-detail/<int:screening_id>/", GetScreeningDetailAPIView.as_view(), name="get-screening-detail"),
]