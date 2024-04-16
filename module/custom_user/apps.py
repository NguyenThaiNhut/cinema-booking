from django.apps import AppConfig
from rest_framework import routers


class CustomUserConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "module.custom_user"
