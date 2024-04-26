from django.contrib.auth.models import AbstractUser, Group, Permission
from django.db import models
from module.hall.models import Cinema

class CustomUser(AbstractUser):
    avatar = models.TextField(blank=True, null=True)
    dob = models.DateField(blank=True, null=True)
    phone_number = models.CharField(max_length=15, blank=False, null=False)
    stripe_customer_id  = models.CharField(max_length=255, blank=True, null=True)
    stripe_pm_id = models.CharField(max_length=255, blank=True, null=True)
    stripe_account_id = models.CharField(max_length=255, blank=True, null=True)
    address_id  = models.CharField(max_length=255, blank=True, null=True)

    # def __str__(self) -> str:
    #     return self.phone_number

    # groups = models.ManyToManyField(Group, related_name="custom_users", blank=True)
    # user_permissions = models.ManyToManyField(
    #     Permission, related_name="custom_users", blank=True
    # )

class UserFavoriteCinema(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    cinema = models.ForeignKey(Cinema, on_delete=models.CASCADE)

    class Meta:
        unique_together = ("user", "cinema")

    def __str__(self):
        return f"{self.user.username}'s favorite cinema: {self.cinema.name}"