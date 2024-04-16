from django.urls import path

from .views import CreateHallAPIView, CinemaBrandAPIView

urlpatterns = [
    path("admin-user/hall/add-hall/", CreateHallAPIView.as_view(), name="add-hall"),
    path("admin-user/cinema/brand/get-brand-by-id/<str:brand_id>/", CinemaBrandAPIView.as_view(), name="get-brand-by-id"), 
    path("admin-user/cinema/brand/add-brand/", CinemaBrandAPIView.as_view(), name="get-brand-by-id"),

    # path("admin-user/movie/add-movie/", CreateMovieAPIView.as_view(), name="add-movie"),
    # path("admin-user/movie/edit-movie/<int:pk>/", EditMovieAPIView.as_view(), name="edit-movie"),
    # path("admin-user/movie/delete-movie/<int:pk>/", DeleteMovieAPIView.as_view(), name="delete-movie"),
    # path("admin-user/movie/search/", SearchMovieAPIView.as_view(), name="search-movie"),
    # path("admin-user/movie/filter/", FilterMovieAPIView.as_view(), name="filter-movie"),
]