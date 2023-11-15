from django.contrib.auth.backends import ModelBackend
from django.contrib.auth import get_user_model

class UsuarioBackend(ModelBackend):
    def get_user(self, user_id):
        UserModel = get_user_model()
        try:
            return UserModel.objects.get(pk=user_id)
        except UserModel.DoesNotExist:
            return None
