from django.db import models

from users.models import User


# Create your models here.
class Habit(models.Model):
    """
    Модель привычки:
    Пользователь — создатель привычки.
    Место — место, в котором необходимо выполнять привычку.
    Время — время, когда необходимо выполнять привычку.
    Действие — действие, которое представляет собой привычка.
    Признак приятной привычки — привычка, которую можно привязать к выполнению полезной привычки.
    Связанная привычка — привычка, которая связана с другой привычкой, важно указывать для полезных привычек, но не для приятных.
    Периодичность (по умолчанию ежедневная) — периодичность выполнения привычки для напоминания в днях.
    Вознаграждение — чем пользователь должен себя вознаградить после выполнения.
    Время на выполнение — время, которое предположительно потратит пользователь на выполнение привычки.
    Признак публичности — привычки можно публиковать в общий доступ, чтобы другие пользователи могли брать в пример чужие привычки.
    """

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name="Пользователь",
        help_text="Укажите пользователя (создателя привычки)",
        related_name="habits",
    )  # удалили пользователя - удалились все его привычки
    place = models.CharField(
        max_length=100,
        verbose_name="Место",
        help_text="Укажите место, в котором необходимо выполнять привычку",
    )
    time = models.TimeField(
        verbose_name="Время", help_text="Время, когда необходимо выполнять привычку"
    )
    action = models.CharField(
        max_length=250,
        verbose_name="Действие",
        help_text="Действие, которое представляет собой привычка",
    )
    is_nice = models.BooleanField(
        default=False,
        verbose_name="Признак приятной привычки",
        help_text="Отметьте, если привычка приятная, но не полезная",
    )  # True - приятная, False - полезная
    related_habit = models.ForeignKey(
        "Habit",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name="Связанная привычка",
        help_text="Укажите приятную привычку, которая связана с полезной привычкой",
    )  # удалили связанную привычку, основная осталась, связь исчезла
    periodicity = models.PositiveIntegerField(
        default=1,
        verbose_name="Периодичность",
        help_text="Укажите периодичность выполнения привычки для напоминания в днях",
    )
    reward = models.CharField(
        max_length=250,
        verbose_name="Вознаграждение",
        blank=True,
        help_text="Укажите вознаграждение после выполнения привычки",
    )
    lasting = models.PositiveIntegerField(
        verbose_name="Время на выполнение",
        help_text="Укажите предположительное время на выполнение привычки в секундах",
    )
    is_public = models.BooleanField(
        default=False,
        verbose_name="Признак публичности",
        help_text="Отметьте, если привычку можно опубликовать в общий доступ",
    )

    def __str__(self):
        return f"{self.user}: {self.time} - {self.action}"

    class Meta:
        verbose_name = "Привычка"
        verbose_name_plural = "Привычки"
