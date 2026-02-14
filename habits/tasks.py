from celery import shared_task

from django.utils import timezone
from habits.models import Habit
from habits.services import send_telegram_message
from users.models import User


@shared_task
def send_telegram_reminder(habit_id, user_id):
    """ Напоминание о привычке """
    habit = Habit.objects.get(id=habit_id)
    user = User.objects.get(id=user_id)

    message = (
        f"""
Напоминание о привычке!
Действие: {habit.action}
Время: {habit.time}
Место: {habit.place}
Длительность: {habit.lasting} сек
        """
    )

    if user.tg_chat_id:
        print(user.tg_chat_id)
        send_telegram_message(user.tg_chat_id, message)


@shared_task
def check_habits_for_reminders():
    now = timezone.localtime()

    habits = Habit.objects.filter(
        time__hour=now.hour,
        time__minute=now.minute,
        user__tg_chat_id__isnull=False
    )

    for habit in habits:
        send_telegram_reminder.delay(habit.id, habit.user_id)
