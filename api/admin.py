from django.contrib import admin

# Register your models here.
from .user_admin import CustomUserAdmin
from .models import CustomUser
admin.site.register(CustomUser,CustomUserAdmin)
