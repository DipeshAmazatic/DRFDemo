from django.contrib.auth.hashers import check_password
from .models import CustomUser
from django.db.models import Q

class EmailOrPhone():
    def authenticate(self,request, username=None, password=None,**kwargs):
        try:
            # Check if the user exists in CustomUser database
            user = CustomUser.objects.get(Q(email=username)|Q(phone_no=username))
            if check_password(password, user.password):
                return user
        except CustomUser.DoesNotExist:
            pass
        return None

    # Required for the backend to work properly - unchanged in most scenarios
    def get_user(self, user_id):
        try:
            user = CustomUser.objects.get(pk=user_id)
        except CustomUser.DoesNotExist:
            return None
        return user if user.is_active else None