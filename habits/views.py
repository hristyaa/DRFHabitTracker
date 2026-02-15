from rest_framework.generics import ListAPIView
from rest_framework.permissions import AllowAny
from rest_framework.viewsets import ModelViewSet

from habits.models import Habit
from habits.paginators import CustomPagination
from habits.serializers import HabitSerializer


class HabitViewSet(ModelViewSet):
    """CRUD для модели привычек с помощью ViewSet (для привычек пользователя)"""

    queryset = Habit.objects.all()
    serializer_class = HabitSerializer
    pagination_class = CustomPagination

    def get_queryset(self):
        if getattr(self, "swagger_fake_view", False):
            return Habit.objects.none()

        user = self.request.user
        if not user.is_authenticated:
            return Habit.objects.none()

        return Habit.objects.filter(user=user)

    def perform_create(self, serializer):
        """Пользователь = создатель привычки"""
        serializer.save(user=self.request.user)


class PublicHabitListAPIView(ListAPIView):
    """Класс для списка публичных привычек"""

    queryset = Habit.objects.filter(is_public=True)
    permission_classes = [AllowAny]
    serializer_class = HabitSerializer
    pagination_class = CustomPagination
