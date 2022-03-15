from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.forms import UserCreationForm,UserChangeForm
from .models import CustomUser

class CustomUserAdmin(UserAdmin):
    add_form = UserCreationForm
    form = UserChangeForm
    model = CustomUser
    list_display = ['pk','email']
    extra_kwargs = {
            'is_email_verified': {'read_only': True}
        }
    add_fieldsets = UserAdmin.add_fieldsets + (
        (None,{'fields':('name','phone_no',)}),
    )
    fieldsets = UserAdmin.fieldsets+(
        (None,{'fields':('name','phone_no','is_email_verified')}),
    )