from rest_framework import serializers
from .models import Exercises, WorkoutSessions, WorkoutSets
from .models import (
    TrainingPlans, PlanDays, PlanDayExercises,
    Measurements, PersonalRecords,
    WorkoutTemplates, TemplateExercises
)
from .models import TrainingPlans, PlanDays, PlanDayExercises

class ExerciseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Exercises
        fields = [
            "id",
            "name",
            "category",
            "description",
            "video_url",
            "is_default",
        ]
        read_only_fields = ["id", "is_default"]

    def validate_name(self, value):
        value = (value or "").strip()
        if not value:
            raise serializers.ValidationError("Nazwa ćwiczenia jest wymagana.")
        return value

class WorkoutSessionSerializer(serializers.ModelSerializer):
    class Meta:
        model = WorkoutSessions
        fields = "__all__"
        read_only_fields = ("user",)

class WorkoutSetSerializer(serializers.ModelSerializer):
    class Meta:
        model = WorkoutSets
        fields = "__all__"


class TrainingPlanSerializer(serializers.ModelSerializer):
    class Meta:
        model = TrainingPlans
        fields = ["id", "name", "created_at"]

class PlanDaySerializer(serializers.ModelSerializer):
    class Meta:
        model = PlanDays
        fields = ["id", "plan_id", "day_name", "position"]


class PlanDayExerciseSerializer(serializers.ModelSerializer):
    exercise_name = serializers.CharField(source="exercise.name", read_only=True)

    class Meta:
        model = PlanDayExercises
        fields = [
            "id",
            "plan_day_id",
            "exercise_id",
            "exercise_name",
            "target_sets",
            "target_reps",
            "position",
        ]

class MeasurementSerializer(serializers.ModelSerializer):
    class Meta:
        model = Measurements
        fields = "__all__"
        read_only_fields = ("user",)

class PersonalRecordSerializer(serializers.ModelSerializer):
    class Meta:
        model = PersonalRecords
        fields = "__all__"
        read_only_fields = ("user",)

class WorkoutTemplateSerializer(serializers.ModelSerializer):
    class Meta:
        model = WorkoutTemplates
        fields = "__all__"
        read_only_fields = ("user",)

class TemplateExerciseSerializer(serializers.ModelSerializer):
    class Meta:
        model = TemplateExercises
        fields = "__all__"