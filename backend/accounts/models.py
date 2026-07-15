from django.db import models
from django.contrib.auth.models import AbstractUser
from phonenumber_field.modelfields import PhoneNumberField

class User(AbstractUser):
    email = models.EmailField(unique=True)

    phone_number = PhoneNumberField(
        unique=True,
        blank=True,
        null=True
    )

    is_verified = models.BooleanField(default = False)

    created_at = models.DateTimeField(auto_now=False, auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True, auto_now_add=False)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["username"]