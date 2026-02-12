from rest_framework import serializers
from habits.models import Habit


class HabitSerializer(serializers.ModelSerializer):

    def validate(self, attrs):

        if "lasting" in attrs:
            lasting = attrs["lasting"]
        elif self.instance:
            lasting = self.instance.lasting

        if "periodicity" in attrs:
            periodicity = attrs["periodicity"]
        elif self.instance:
            periodicity = self.instance.periodicity
        else:
            periodicity = 1

        if 'related_habit' in attrs:
            related_habit = attrs["related_habit"]
        elif self.instance:
            related_habit = self.instance.related_habit
        else:
            related_habit = None

        if 'reward' in attrs:
            reward = attrs["reward"]
        elif self.instance:
            reward = self.instance.reward
        else:
            reward = ""

        if 'is_nice' in attrs:
            is_nice = attrs["is_nice"]
        elif self.instance:
            is_nice = self.instance.is_nice
        else:
            is_nice = False

        # валидация
        if lasting is not None:
            if lasting > 120:
                raise serializers.ValidationError("Время выполнения должно быть не больше 120 секунд")

        if periodicity > 7 or periodicity < 1:
            raise serializers.ValidationError("Периодичность должна быть от 1 до 7 дней")

        if related_habit is not None and reward.strip():
            raise serializers.ValidationError("У привычки не может быть одновременно вознаграждения и связанной привычки, выберите что-то одно")

        if is_nice and (related_habit is not None or reward.strip()):
            raise serializers.ValidationError("У приятной привычки не может быть вознаграждения или связанной привычки.")

        if related_habit is not None and not related_habit.is_nice:
            raise serializers.ValidationError("Связанная привычка должна быть приятной")

        return attrs

    class Meta:
        model = Habit
        fields = "__all__"
        read_only_fields = ["user"]  # пользователь не может вводить владельца сам
