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

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["username"]

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE , related_name='profile')
    dob = models.DateField()
    
    class Gender(models.TextChoices):
        MALE = "Male", "Male"
        FEMALE = "Female", "Female"

    gender = models.CharField(
        max_length=50,
        choices=Gender.choices
        )
    
    created_at = models.DateTimeField(auto_now=False, auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True, auto_now_add=False)

class Address(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE , related_name='addresses')

    full_name = models.CharField(max_length=50)

    phone = PhoneNumberField()

    address_line_1 = models.CharField(max_length=255)

    address_line_2 = models.CharField(max_length=50,blank=True)

    city = models.CharField(max_length=100)

    state = models.CharField(max_length=50)

    postal_code = models.CharField(max_length=50)

    country = models.CharField(max_length=50)