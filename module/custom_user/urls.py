from django.urls import path
from .views import (
    RegistrationAPIView, LoginAPIView, LogoutAPIView, 
    ProfileAPIView, EditProfileAPIView, 
    ImageUploadAPIView, RefreshTokenAPIView
)

urlpatterns = [
    path("register/", RegistrationAPIView.as_view(), name="register"),
    path("login/", LoginAPIView.as_view(), name="login"),
    path('logout/', LogoutAPIView.as_view(), name='logout'),
    path("profile/", ProfileAPIView.as_view(), name="profile"),
    path("profile/edit/", EditProfileAPIView.as_view(), name="edit-profile"),
    path('upload/', ImageUploadAPIView.as_view(), name='image-upload'),
    path('token/refresh/', RefreshTokenAPIView.as_view(), name='token_refresh'),

    # path('upload-image/', UploadImageView.as_view(), name='upload-image'),
    # path("film/", EditProfileAPIView.as_view(), name="edit-profile"),
    # path("admin-user/film/", EditProfileAPIView.as_view(), name="edit-profile"),
    # path("admin-user", EditProfileAPIView.as_view(), name="edit-profile"),
    # path("admin-user/account", EditProfileAPIView.as_view(), name="edit-profile"),
    # path("admin-user/hall/create-hall", EditProfileAPIView.as_view(), name="edit-profile"),
]
