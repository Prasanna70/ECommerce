from django.contrib.auth.backends import BaseBackend
from apps.ecommerce_admin.models import Admin
from django.db import models 
class CRNEmailMobileAuthBackend(BaseBackend):
    def authenticate(self, request, username=None, password=None, **kwargs):
        user = Admin.objects.filter(
            models.Q(email=username) | 
            models.Q(mobile=username) | 
            models.Q(crn=username)
        ).first()

        if user and user.check_password(password):
            return user
        return None

    def get_user(self, user_id):
        try:
            return Admin.objects.get(pk=user_id)
        except Admin.DoesNotExist:
            return None

