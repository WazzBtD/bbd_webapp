from django.contrib.auth.backends import ModelBackend
from django.conf import settings
from django.core.exceptions import ObjectDoesNotExist
from main.models import MyUser


class CustomAuthBackend(ModelBackend):
    def authenticate(self, request, username=None, password=None, **kwargs):
        try:
            user = MyUser.objects.using(settings.ADMIN_DB).get(username=username)
        except ObjectDoesNotExist:
            return None
        if user.check_password(password) and self.user_can_authenticate(user):
            return user
        return None

    def get_user(self, user_id):
        try:
            return MyUser.objects.using(settings.ADMIN_DB).get(pk=user_id)
        except MyUser.DoesNotExist:
            return None