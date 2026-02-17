from django.contrib.auth import get_user_model
from django.contrib.auth.backends import ModelBackend

User = get_user_model()

class EmailOrPhoneBackend(ModelBackend):
    """
    Authenticate using either email or phone number.
    """
    def authenticate(self, request, username=None, password=None, **kwargs):
        if username is None:
            username = kwargs.get('phone') or kwargs.get('email')
        
        try:
            # Check by email first
            user = User.objects.get(email=username)
        except User.DoesNotExist:
            try:
                # Check by phone
                user = User.objects.get(phone=username)
            except User.DoesNotExist:
                return None
        
        if user.check_password(password) and self.user_can_authenticate(user):
            return user
        return None
