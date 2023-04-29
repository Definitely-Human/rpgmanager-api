"""
Database models.
"""

from django.db import models
from django.contrib.auth.models import{
    AbstractBaseUser,
    BaseUserManager,
    PermissionsMixin,
}
from django.utils import timezone

class User(AbstractBaseUser, PermissionsMixin):
    """User in the system"""
    email = models.EmailField(max_length=255, unique=True)
    username = models.CharField(max_length=50, unique=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    date_joined = models.DateTimeField(default=timezone.now)

    USERNAME_FIELD = 'email'