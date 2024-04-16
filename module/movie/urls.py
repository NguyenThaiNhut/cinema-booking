from django.urls import path

from .views import ListMovieAPIView, CreateMovieAPIView, EditMovieAPIView, DeleteMovieAPIView, SearchMovieAPIView, FilterMovieAPIView

urlpatterns = [
    path("admin-user/movie/get-movie-list/", ListMovieAPIView.as_view(), name="get-movie-list"),
    path("admin-user/movie/add-movie/", CreateMovieAPIView.as_view(), name="add-movie"),
    path("admin-user/movie/edit-movie/<int:pk>/", EditMovieAPIView.as_view(), name="edit-movie"),
    path("admin-user/movie/delete-movie/<int:pk>/", DeleteMovieAPIView.as_view(), name="delete-movie"),
    path("admin-user/movie/search/", SearchMovieAPIView.as_view(), name="search-movie"),
    path("admin-user/movie/filter/", FilterMovieAPIView.as_view(), name="filter-movie"),
]
