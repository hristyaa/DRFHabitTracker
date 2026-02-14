from rest_framework.generics import CreateAPIView
from rest_framework.permissions import AllowAny

from users.models import User
from users.serializers import UserSerializer


class UserCreateAPIView(CreateAPIView):
    """Эндпоинт для создания пользователя"""

    serializer_class = UserSerializer
    queryset = User.objects.all()
    permission_classes = (AllowAny,)  # доступен без авторизации

    def perform_create(self, serializer):
        user = serializer.save(is_active=True)
        user.set_password(user.password)  # хэшированеи пароля
        user.save()
