from django.contrib.auth.models import AbstractUser
from django.db import models
from api.accounts.managers import CustomUserManager
from django.utils.translation import gettext_lazy as _


class User(AbstractUser):
    username = (None,)
    email = models.EmailField(_("email address"), blank=True, unique=True)
    name = models.CharField(max_length=20, null=True)
    phone_number = models.CharField(max_length=20, null=True)
    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []
    profile_image = models.FileField(
        blank=True,
        null=True,
    )
    nickname = models.CharField(max_length=20, null=True)
    objects = CustomUserManager()

    def __str__(self):
        return self.email

    class Meta:
        db_table = "sww_user"
        ordering = ["-id"]
