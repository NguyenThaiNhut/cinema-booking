from django.urls import path

from .views import (
    ListMovieAPIView, MovieAPIView, SearchMovieAPIView, FilterMovieAPIView,
    GetListCurrentShowingMovieAPIView, GetListUpcomingMovieAPIView, GetListFeatureMovieAPIView, DetailMovieAPIView
)

urlpatterns = [
    path("admin-user/movie/get-movie-by-id/<str:movie_id>/", ListMovieAPIView.as_view(), name="get-movie-list"),
    path("admin-user/movie/add-movie/", MovieAPIView.as_view(), name="add-movie"),
    path("admin-user/movie/edit-movie/<int:movie_id>/", MovieAPIView.as_view(), name="edit-movie"),
    path("admin-user/movie/delete-movie/<int:movie_id>/", MovieAPIView.as_view(), name="delete-movie"),
    path("admin-user/movie/search/", SearchMovieAPIView.as_view(), name="search-movie"),
    path("admin-user/movie/filter/", FilterMovieAPIView.as_view(), name="filter-movie"),

    path("movie/get-list-current-showing-movie/", GetListCurrentShowingMovieAPIView.as_view(), name="get-list-current-showing-movie"),
    path("movie/get-list-upcoming-movie/", GetListUpcomingMovieAPIView.as_view(), name="get-list-upcoming-movie"),
    path("movie/get-list-feature-movie/", GetListFeatureMovieAPIView.as_view(), name="get-list-feature-movie"),
    path("movie/detail/<str:movie_id>/", DetailMovieAPIView.as_view(), name="get-detail-movie"),
]
