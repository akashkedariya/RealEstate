from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import gettext_lazy as _

from django.contrib.auth.base_user import BaseUserManager
from django.utils.translation import gettext_lazy as _
from django.core.validators import RegexValidator


class CustomUserManager(BaseUserManager):
    """
    Custom user model manager where email is the unique identifiers
    for authentication instead of usernames.
    """
    def create_user(self, email, password, **extra_fields):
        """
        Create and save a user with the given email and password.
        """
        if not email:
            raise ValueError(_("The Email must be set"))
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, email, password, **extra_fields):
        """
        Create and save a SuperUser with the given email and password.
        """
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        extra_fields.setdefault("is_active", True)

        if extra_fields.get("is_staff") is not True:
            raise ValueError(_("Superuser must have is_staff=True."))
        if extra_fields.get("is_superuser") is not True:
            raise ValueError(_("Superuser must have is_superuser=True."))
        return self.create_user(email, password, **extra_fields)



class CustomUser(AbstractUser):
    username = None
    email = models.EmailField(_("email address"), unique=True)
    phone_number = models.CharField(
        max_length=10, 
        validators=[RegexValidator(regex=r'^\d{10}$', message="Phone number must be 10 digits")]
    )

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    objects = CustomUserManager()

    def __str__(self):
        return self.email


# class Property(models.Model):
#     PROPERTY_TYPES = [
#         ('house', 'House'),
#         ('apartment', 'Apartment'),
#         ('commercial', 'Commercial'),
#     ]
    
#     title = models.CharField(max_length=255)
#     description = models.TextField()
#     price = models.DecimalField(max_digits=10, decimal_places=2)
#     property_type = models.CharField(choices=PROPERTY_TYPES, max_length=50)
#     location = models.CharField(max_length=255)
#     bedrooms = models.IntegerField()
#     bathrooms = models.IntegerField()
#     square_feet = models.IntegerField()
#     image = models.ImageField(upload_to='property_images/')
#     created_at = models.DateTimeField(auto_now_add=True)
    
#     def __str__(self):
#         return self.title        
