from django.db import models
from django.contrib.auth.models import User
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.base_user import BaseUserManager
from django.utils.translation import gettext_lazy as _
from django.core.validators import RegexValidator


class Country(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name


class City(models.Model):
    city = models.CharField(max_length=50, blank=True)
    country = models.ForeignKey(Country, on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return self.city


class CustomUserManager(BaseUserManager):
    def create_user(self, password, **extra_fields):
        user = self.model(**extra_fields)
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, password, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError(_('Superuser must have is_staff=True.'))
        if extra_fields.get('is_superuser') is not True:
            raise ValueError(_('Superuser must have is_superuser=True.'))
        return self.create_user(password, **extra_fields)


class CustomUser(AbstractUser):
    USER_TYPE_CHOICES = (
        (1, 'client'),
        (2, 'company'),
    )
    email = models.EmailField(_('email address'), unique=True)
    user_type = models.PositiveSmallIntegerField(choices=USER_TYPE_CHOICES, default=1)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_superuser = models.BooleanField(default=False)
    objects = CustomUserManager()
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []
    username = None


class Client(CustomUser):
    city = models.ForeignKey(City, on_delete=models.CASCADE, null=True, blank=True, default=1)
    regex = RegexValidator(regex=r'^\+?77([0124567][0-8]\d{7})$')
    phone = models.CharField(validators=[regex], unique=True, max_length=12)
    cv = models.FileField(upload_to='cv/', null=True, blank=True)
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []
    username = None

    def __str__(self):
        return self.first_name, self.last_name


class Company(CustomUser):
    city = models.ForeignKey(City, on_delete=models.CASCADE, null=True, blank=True, default=1)
    company_name = models.CharField(max_length=50)
    company_description = models.TextField(max_length=500)
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []
    username = None
    first_name = None
    last_name = None

    def __str__(self):
        return self.company_name
