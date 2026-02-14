from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from habits.models import Habit
from users.models import User

# Create your tests here.


class HabitTestCase(APITestCase):

    def setUp(self):
        self.user = User.objects.create(email="test@test.ru")
        self.user.set_password("1234")
        self.habit = Habit.objects.create(
            user=self.user,
            place="кухня",
            time="08:00:00",
            action="Пить теплую воду",
            reward="Час просмотра любимого сериала",
            lasting=30,
        )
        self.habit_2 = Habit.objects.create(
            user=self.user, place="test", time="08:00:00", action="test", lasting=30
        )
        self.related_habit = Habit.objects.create(
            user=self.user,
            place="test",
            time="08:00:00",
            action="test related_habit",
            lasting=30,
            is_nice=True,
        )
        self.client.force_authenticate(user=self.user)

    def test_habit_get(self):
        """Тестирование детального просмотра привычки"""
        url = reverse("habits:habit-detail", args=[self.habit.id])
        response = self.client.get(url)
        data = response.json()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(data.get("action"), self.habit.action)
        self.assertEqual(data.get("reward"), self.habit.reward)

    def test_habit_create(self):
        """Тестирование создания привычки"""
        url = reverse("habits:habit-list")
        data = {
            "place": "Test",
            "time": "08:30:00",
            "action": "Test action",
            "reward": "Test reward",
            "lasting": 30,
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Habit.objects.count(), 4)

    def _assert_patch_400(self, url, data, validate_error):
        """Метод для проверки ошибки валидации в test_habit_partial_update"""
        response = self.client.patch(url, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.json().get("non_field_errors"), [validate_error])

    def test_habit_partial_update(self):
        """Тестирование валидации при частичном обновлении привычки"""
        url = reverse("habits:habit-detail", args=[self.habit.id])
        data = {"is_nice": True}
        self._assert_patch_400(
            url,
            data,
            "У приятной привычки не может быть вознаграждения или связанной привычки.",
        )
        data = {"lasting": 125}
        self._assert_patch_400(
            url, data, "Время выполнения должно быть не больше 120 секунд"
        )
        data = {"periodicity": 10}
        self._assert_patch_400(url, data, "Периодичность должна быть от 1 до 7 дней")
        data = {"related_habit": self.related_habit.id}
        self._assert_patch_400(
            url,
            data,
            "У привычки не может быть одновременно вознаграждения и связанной привычки, выберите что-то одно",
        )
        data = {"reward": "", "related_habit": self.habit_2.id}
        self._assert_patch_400(url, data, "Связанная привычка должна быть приятной")
        data = {
            "reward": "",
            "related_habit": self.related_habit.id,
        }  # валидация проходит
        response = self.client.patch(url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(data.get("related_habit"), self.related_habit.id)
        self.assertEqual(data.get("reward"), "")

    def test_habit_delete(self):
        """Тестирование удаления привычки"""
        url = reverse("habits:habit-detail", args=(self.habit_2.id,))
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Habit.objects.count(), 2)

    def test_habit_list(self):
        """Тестирование просмотра списка привычек"""
        url = reverse("habits:habit-list")
        response = self.client.get(url)
        data = response.json()
        result = [
            {
                "id": self.habit.id,
                "place": self.habit.place,
                "time": self.habit.time,
                "action": self.habit.action,
                "is_nice": False,
                "periodicity": self.habit.periodicity,
                "reward": self.habit.reward,
                "lasting": self.habit.lasting,
                "is_public": False,
                "user": self.user.id,
                "related_habit": None,
            },
            {
                "id": self.habit_2.id,
                "place": self.habit_2.place,
                "time": self.habit_2.time,
                "action": self.habit_2.action,
                "is_nice": False,
                "periodicity": self.habit_2.periodicity,
                "reward": "",
                "lasting": self.habit_2.lasting,
                "is_public": False,
                "user": self.user.id,
                "related_habit": None,
            },
            {
                "id": self.related_habit.id,
                "place": self.related_habit.place,
                "time": self.related_habit.time,
                "action": self.related_habit.action,
                "is_nice": self.related_habit.is_nice,
                "periodicity": self.related_habit.periodicity,
                "reward": "",
                "lasting": self.related_habit.lasting,
                "is_public": False,
                "user": self.user.id,
                "related_habit": None,
            },
        ]

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(data, result)
