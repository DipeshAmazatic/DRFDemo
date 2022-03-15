from django.db import models

# Create your models here.
from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext_lazy as _
from .manager import CustomUserManager

class CustomUser(AbstractUser):
    username = models.CharField(_('username'),max_length=150,blank=True,null=True)
    name = models.CharField(max_length=30)
    email = models.EmailField(max_length=30,unique=True)
    phone_no = models.CharField(max_length=10,unique=True)
    is_email_verified = models.BooleanField(default=False)
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['phone_no']
    objects = CustomUserManager()

    def __str__(self):
        return str(self.email)