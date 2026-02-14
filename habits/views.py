from rest_framework.viewsets import ModelViewSet

from habits.models import Habit
from habits.paginators import CustomPagination
from habits.serializers import HabitSerializer


class HabitViewSet(ModelViewSet):
    """CRUD для модели привычек с помощью ViewSet"""

    queryset = Habit.objects.all()
    serializer_class = HabitSerializer
    pagination_class = CustomPagination

    def perform_create(self, serializer):
        """Пользователь = создатель привычки"""
        serializer.save(user=self.request.user)
