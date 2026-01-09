from django.contrib import admin
from . import models


@admin.register(models.Exercises)
class ExercisesAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "category", "user", "is_default")
    list_filter = ("category", "is_default")
    search_fields = ("name", "category", "user__username")
    ordering = ("name",)


@admin.register(models.WorkoutSessions)
class WorkoutSessionsAdmin(admin.ModelAdmin):
    list_display = ("id", "user", "date", "duration_minutes", "plan_day")
    list_filter = ("user",)
    search_fields = ("user__username", "notes")
    ordering = ("-date",)


@admin.register(models.WorkoutSets)
class WorkoutSetsAdmin(admin.ModelAdmin):
    list_display = ("id", "session", "exercise", "set_number", "weight", "reps", "rir", "created_at")
    list_filter = ("exercise",)
    search_fields = ("exercise__name",)
    ordering = ("-created_at",)


@admin.register(models.TrainingPlans)
class TrainingPlansAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "user", "created_at")
    list_filter = ("user",)
    search_fields = ("name", "user__username")
    ordering = ("-created_at",)


@admin.register(models.PlanDays)
class PlanDaysAdmin(admin.ModelAdmin):
    list_display = ("id", "plan", "day_name", "position")
    list_filter = ("plan",)
    ordering = ("plan", "position")


@admin.register(models.PlanDayExercises)
class PlanDayExercisesAdmin(admin.ModelAdmin):
    list_display = ("id", "plan_day", "exercise", "target_sets", "target_reps", "position")
    list_filter = ("plan_day",)
    search_fields = ("exercise__name",)
    ordering = ("plan_day", "position")


@admin.register(models.Measurements)
class MeasurementsAdmin(admin.ModelAdmin):
    list_display = ("id", "user", "date", "weight", "body_fat", "waist", "chest", "arms", "hips")
    list_filter = ("user",)
    ordering = ("-date",)


@admin.register(models.PersonalRecords)
class PersonalRecordsAdmin(admin.ModelAdmin):
    list_display = ("id", "user", "exercise", "weight", "reps", "estimated_1rm", "achieved_at")
    list_filter = ("user", "exercise")
    search_fields = ("exercise__name", "user__username")
    ordering = ("-achieved_at",)


@admin.register(models.WorkoutTemplates)
class WorkoutTemplatesAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "user", "created_at")
    list_filter = ("user",)
    search_fields = ("name", "user__username")
    ordering = ("-created_at",)


@admin.register(models.TemplateExercises)
class TemplateExercisesAdmin(admin.ModelAdmin):
    list_display = ("id", "template", "exercise", "target_sets", "target_reps", "position")
    list_filter = ("template",)
    search_fields = ("exercise__name",)
    ordering = ("template", "position")


@admin.register(models.Notifications)
class NotificationsAdmin(admin.ModelAdmin):
    list_display = ("id", "user", "send_at", "created_at", "message")
    list_filter = ("user",)
    ordering = ("-send_at",)


@admin.register(models.UserSettings)
class UserSettingsAdmin(admin.ModelAdmin):
    list_display = ("user", "weight_unit", "distance_unit", "theme")
    list_filter = ("theme", "weight_unit", "distance_unit")


# --- Słowniki / pomocnicze ---
@admin.register(models.Tags)
class TagsAdmin(admin.ModelAdmin):
    list_display = ("id", "name")
    search_fields = ("name",)


@admin.register(models.Muscles)
class MusclesAdmin(admin.ModelAdmin):
    list_display = ("id", "name")
    search_fields = ("name",)


@admin.register(models.Equipment)
class EquipmentAdmin(admin.ModelAdmin):
    list_display = ("id", "name")
    search_fields = ("name",)
