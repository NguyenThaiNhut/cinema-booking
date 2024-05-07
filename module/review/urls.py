from django.urls import path

from .views import (
    GetListReviewTagAPIView, ReviewTagAPIView, 
    GetMovieReviewsAPIView, ReviewAPIView, 
)

urlpatterns = [
    # api of admin
    path("admin-user/review-tag/get-tag-by-id/<str:tag_id>/", GetListReviewTagAPIView.as_view(), name="get-tag-by-id"), 
    path("admin-user/review-tag/add-tag/", ReviewTagAPIView.as_view(), name="add-tag"),
    path("admin-user/review-tag/update-tag/<int:tag_id>/", ReviewTagAPIView.as_view(), name="update-tag"),
    path("admin-user/review-tag/delete-tag/<int:tag_id>/", ReviewTagAPIView.as_view(), name="delete-tag"),

    path("review/get-reviews-by-id-movie/<int:movie_id>/", GetMovieReviewsAPIView.as_view(), name="get-reviews-by-id-movie"),
    path("review/create-review/", ReviewAPIView.as_view(), name="create-review"),
    path("review/update-review/<int:review_id>/", ReviewAPIView.as_view(), name="update-review"),
]