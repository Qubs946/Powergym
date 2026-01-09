from django.contrib import admin
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from gym.views import ExerciseViewSet, WorkoutSessionViewSet, WorkoutSetViewSet
from gym.views import (
    ExerciseViewSet, WorkoutSessionViewSet, WorkoutSetViewSet,
    TrainingPlanViewSet, PlanDayViewSet, PlanDayExerciseViewSet,
    MeasurementViewSet, PersonalRecordViewSet,
    WorkoutTemplateViewSet, TemplateExerciseViewSet
)
from gym.views import register
from gym.views import exercises_view
from gym.views import plans_view, plan_days_view, plan_day_exercises_view


router = DefaultRouter()
router.register(r"exercises", ExerciseViewSet, basename="exercises")
router.register(r"workout-sessions", WorkoutSessionViewSet, basename="workout-sessions")
router.register(r"workout-sets", WorkoutSetViewSet, basename="workout-sets")
router.register(r"training-plans", TrainingPlanViewSet, basename="training-plans")
router.register(r"plan-days", PlanDayViewSet, basename="plan-days")
router.register(r"plan-day-exercises", PlanDayExerciseViewSet, basename="plan-day-exercises")

router.register(r"measurements", MeasurementViewSet, basename="measurements")
router.register(r"personal-records", PersonalRecordViewSet, basename="personal-records")

router.register(r"workout-templates", WorkoutTemplateViewSet, basename="workout-templates")
router.register(r"template-exercises", TemplateExerciseViewSet, basename="template-exercises")

urlpatterns = [
    path("admin/", admin.site.urls),
    path("register/", register),
    path("api/auth/register/", register, name="register"),
    path("api/exercises/", exercises_view),

    path("api/auth/token/", TokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("api/auth/refresh/", TokenRefreshView.as_view(), name="token_refresh"),

    path("api/", include(router.urls)),
    path("api-auth/", include("rest_framework.urls")),

    path("api/plans/", plans_view),
    path("api/plans/<int:plan_id>/days/", plan_days_view),
    path("api/plan-days/<int:plan_day_id>/exercises/", plan_day_exercises_view),
]
