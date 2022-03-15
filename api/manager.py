from django.contrib.auth.models import UserManager
from django.contrib.auth.hashers import make_password

class CustomUserManager(UserManager):
    def _create_user(self,username, email, password, **extra_fields):    
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.password = make_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, username=None, email=None, password=None, **extra_fields):
        return super().create_user(email=email, password=password, **extra_fields)

    def create_superuser(self,username=None, email=None, password=None, **extra_fields):
        return super().create_superuser(username=None,email=email, password=password, **extra_fields)