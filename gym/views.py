from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from .models import Exercises, WorkoutSessions, WorkoutSets
from .serializers import ExerciseSerializer, WorkoutSessionSerializer, WorkoutSetSerializer
from .models import (
    TrainingPlans, PlanDays, PlanDayExercises,
    Measurements, PersonalRecords,
    WorkoutTemplates, TemplateExercises
)
from .serializers import (
    TrainingPlanSerializer, PlanDaySerializer, PlanDayExerciseSerializer,
    MeasurementSerializer, PersonalRecordSerializer,
    WorkoutTemplateSerializer, TemplateExerciseSerializer
)
from django.db.models import Max
from django.contrib.auth.models import User
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework import status


class ExerciseViewSet(viewsets.ModelViewSet):
    serializer_class = ExerciseSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Exercises.objects.filter(user__isnull=True) | Exercises.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

class WorkoutSessionViewSet(viewsets.ModelViewSet):
    serializer_class = WorkoutSessionSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return WorkoutSessions.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

class WorkoutSetViewSet(viewsets.ModelViewSet):
    serializer_class = WorkoutSetSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return WorkoutSets.objects.filter(session__user=self.request.user)


class TrainingPlanViewSet(viewsets.ModelViewSet):
    serializer_class = TrainingPlanSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return TrainingPlans.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

class PlanDayViewSet(viewsets.ModelViewSet):
    serializer_class = PlanDaySerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        # tylko dni należące do planów usera
        return PlanDays.objects.filter(plan__user=self.request.user)

class PlanDayExerciseViewSet(viewsets.ModelViewSet):
    serializer_class = PlanDayExerciseSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        # tylko ćwiczenia w dniach planów usera
        return PlanDayExercises.objects.filter(plan_day__plan__user=self.request.user)

class MeasurementViewSet(viewsets.ModelViewSet):
    serializer_class = MeasurementSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Measurements.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

class PersonalRecordViewSet(viewsets.ModelViewSet):
    serializer_class = PersonalRecordSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return PersonalRecords.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

class WorkoutTemplateViewSet(viewsets.ModelViewSet):
    serializer_class = WorkoutTemplateSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return WorkoutTemplates.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

class TemplateExerciseViewSet(viewsets.ModelViewSet):
    serializer_class = TemplateExerciseSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return TemplateExercises.objects.filter(template__user=self.request.user)


@api_view(["POST"])
@permission_classes([AllowAny])
def register(request):
    username = request.data.get("email")
    password = request.data.get("password")

    if not username or not password:
        return Response(
            {"detail": "Email i hasło są wymagane"},
            status=status.HTTP_400_BAD_REQUEST
        )

    if User.objects.filter(username=username).exists():
        return Response(
            {"detail": "Użytkownik już istnieje"},
            status=status.HTTP_400_BAD_REQUEST
        )

    user = User.objects.create_user(
        username=username,
        email=username,
        password=password
    )

    return Response(
        {"detail": "Użytkownik utworzony"},
        status=status.HTTP_201_CREATED
    )

@api_view(["GET", "POST"])
@permission_classes([IsAuthenticated])
def exercises_view(request):
    if request.method == "GET":
        qs = Exercises.objects.filter(user=request.user) | Exercises.objects.filter(is_default=True)
        qs = qs.distinct().order_by("name")
        return Response(ExerciseSerializer(qs, many=True).data)

    # POST
    serializer = ExerciseSerializer(data=request.data)
    if serializer.is_valid():
        obj = Exercises.objects.create(
            user=request.user,
            name=serializer.validated_data["name"],
            category=serializer.validated_data.get("category"),
            description=serializer.validated_data.get("description"),
            video_url=serializer.validated_data.get("video_url"),
            is_default=False,
        )
        return Response(ExerciseSerializer(obj).data, status=status.HTTP_201_CREATED)

    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(["GET", "POST"])
@permission_classes([IsAuthenticated])
def plans_view(request):
    if request.method == "GET":
        qs = TrainingPlans.objects.filter(user=request.user).order_by("-id")
        return Response(TrainingPlanSerializer(qs, many=True).data)

    # POST create plan
    name = (request.data.get("name") or "").strip()
    if not name:
        return Response({"detail": "name is required"}, status=status.HTTP_400_BAD_REQUEST)

    plan = TrainingPlans.objects.create(user=request.user, name=name)
    return Response(TrainingPlanSerializer(plan).data, status=status.HTTP_201_CREATED)


@api_view(["GET", "POST"])
@permission_classes([IsAuthenticated])
def plan_days_view(request, plan_id: int):
    # sprawdź ownership planu
    try:
        plan = TrainingPlans.objects.get(id=plan_id, user=request.user)
    except TrainingPlans.DoesNotExist:
        return Response({"detail": "Not found"}, status=status.HTTP_404_NOT_FOUND)

    if request.method == "GET":
        days = PlanDays.objects.filter(plan=plan).order_by("position", "id")
        return Response(PlanDaySerializer(days, many=True).data)

    # POST add day
    day_name = (request.data.get("day_name") or "").strip()
    if not day_name:
        return Response({"detail": "day_name is required"}, status=status.HTTP_400_BAD_REQUEST)

    # auto position (ostatni + 1)
    max_pos = PlanDays.objects.filter(plan=plan).aggregate(Max("position"))["position__max"] or 0
    day = PlanDays.objects.create(plan=plan, day_name=day_name, position=max_pos + 1)
    return Response(PlanDaySerializer(day).data, status=status.HTTP_201_CREATED)


@api_view(["GET", "POST"])
@permission_classes([IsAuthenticated])
def plan_day_exercises_view(request, plan_day_id: int):
    # ownership: plan_day -> plan -> user
    try:
        day = PlanDays.objects.select_related("plan").get(id=plan_day_id, plan__user=request.user)
    except PlanDays.DoesNotExist:
        return Response({"detail": "Not found"}, status=status.HTTP_404_NOT_FOUND)

    if request.method == "GET":
        items = PlanDayExercises.objects.filter(plan_day=day).select_related("exercise").order_by("position", "id")
        return Response(PlanDayExerciseSerializer(items, many=True).data)

    # POST add exercise to day
    exercise_id = request.data.get("exercise_id")
    if not exercise_id:
        return Response({"detail": "exercise_id is required"}, status=status.HTTP_400_BAD_REQUEST)

    # ćwiczenie musi być: default albo userowe (Twoje)
    try:
        ex = Exercises.objects.get(id=exercise_id)
    except Exercises.DoesNotExist:
        return Response({"detail": "Exercise not found"}, status=status.HTTP_404_NOT_FOUND)

    if not (ex.is_default or (ex.user_id == request.user.id)):
        return Response({"detail": "Forbidden"}, status=status.HTTP_403_FORBIDDEN)

    target_sets = request.data.get("target_sets")
    target_reps = request.data.get("target_reps")

    # auto position
    max_pos = PlanDayExercises.objects.filter(plan_day=day).aggregate(Max("position"))["position__max"] or 0
    item = PlanDayExercises.objects.create(
        plan_day=day,
        exercise=ex,
        target_sets=target_sets,
        target_reps=target_reps,
        position=max_pos + 1,
    )
    return Response(PlanDayExerciseSerializer(item).data, status=status.HTTP_201_CREATED)