from rest_framework.serializers import ModelSerializer

from users.models import User


class UserSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = ["id", "email", "password", "phone", "tg_nick", "avatar", "tg_chat_id"]
        extra_kwargs = {
            "password": {"write_only": True}
        }  # пароль не выводит в ответах, можно только написать
