from django.urls import path

from .views import ListMovieAPIView, MovieAPIView, SearchMovieAPIView, FilterMovieAPIView

urlpatterns = [
    path("admin-user/movie/get-movie-by-id/<str:movie_id>/", ListMovieAPIView.as_view(), name="get-movie-list"),
    path("admin-user/movie/add-movie/", MovieAPIView.as_view(), name="add-movie"),
    path("admin-user/movie/edit-movie/<int:movie_id>/", MovieAPIView.as_view(), name="edit-movie"),
    path("admin-user/movie/delete-movie/<int:movie_id>/", MovieAPIView.as_view(), name="delete-movie"),
    path("admin-user/movie/search/", SearchMovieAPIView.as_view(), name="search-movie"),
    path("admin-user/movie/filter/", FilterMovieAPIView.as_view(), name="filter-movie"),
]
