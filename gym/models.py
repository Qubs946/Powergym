from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()


class Equipment(models.Model):
    name = models.CharField(unique=True, max_length=100)

    class Meta:
        managed = False
        db_table = "equipment"


class Muscles(models.Model):
    name = models.CharField(unique=True, max_length=100)

    class Meta:
        managed = False
        db_table = "muscles"


class Tags(models.Model):
    name = models.CharField(unique=True, max_length=100)

    class Meta:
        managed = False
        db_table = "tags"


class Exercises(models.Model):
    user = models.ForeignKey(
        User, models.DO_NOTHING, blank=True, null=True, db_column="user_id"
    )
    name = models.CharField(max_length=255)
    category = models.CharField(max_length=100, blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    video_url = models.TextField(blank=True, null=True)
    is_default = models.BooleanField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = "exercises"
        unique_together = (("user", "name"),)


class ExerciseEquipment(models.Model):
    exercise = models.ForeignKey(Exercises, models.DO_NOTHING)
    equipment = models.ForeignKey(Equipment, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = "exercise_equipment"
        unique_together = (("exercise", "equipment"),)


class ExerciseMuscles(models.Model):
    exercise = models.ForeignKey(Exercises, models.DO_NOTHING)
    muscle = models.ForeignKey(Muscles, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = "exercise_muscles"
        unique_together = (("exercise", "muscle"),)


class ExerciseTags(models.Model):
    exercise = models.ForeignKey(Exercises, models.DO_NOTHING)
    tag = models.ForeignKey(Tags, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = "exercise_tags"
        unique_together = (("exercise", "tag"),)


class TrainingPlans(models.Model):
    user = models.ForeignKey(
        User, models.DO_NOTHING, blank=True, null=True, db_column="user_id"
    )
    name = models.CharField(max_length=255)
    created_at = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = "training_plans"


class PlanDays(models.Model):
    plan = models.ForeignKey(TrainingPlans, models.DO_NOTHING, blank=True, null=True)
    day_name = models.CharField(max_length=100)
    position = models.IntegerField()

    class Meta:
        managed = False
        db_table = "plan_days"


class PlanDayExercises(models.Model):
    plan_day = models.ForeignKey(PlanDays, models.DO_NOTHING, blank=True, null=True)
    exercise = models.ForeignKey(Exercises, models.DO_NOTHING, blank=True, null=True)
    target_sets = models.IntegerField(blank=True, null=True)
    target_reps = models.IntegerField(blank=True, null=True)
    position = models.IntegerField()

    class Meta:
        managed = False
        db_table = "plan_day_exercises"


class PlanTags(models.Model):
    plan = models.ForeignKey(TrainingPlans, models.DO_NOTHING)
    tag = models.ForeignKey(Tags, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = "plan_tags"
        unique_together = (("plan", "tag"),)


class WorkoutSessions(models.Model):
    user = models.ForeignKey(
        User, models.DO_NOTHING, blank=True, null=True, db_column="user_id"
    )
    plan_day = models.ForeignKey(PlanDays, models.DO_NOTHING, blank=True, null=True)
    date = models.DateTimeField(blank=True, null=True)
    duration_minutes = models.IntegerField(blank=True, null=True)
    notes = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = "workout_sessions"


class WorkoutSets(models.Model):
    session = models.ForeignKey(WorkoutSessions, models.DO_NOTHING, blank=True, null=True)
    exercise = models.ForeignKey(Exercises, models.DO_NOTHING, blank=True, null=True)
    set_number = models.IntegerField()
    weight = models.DecimalField(max_digits=6, decimal_places=2, blank=True, null=True)
    reps = models.IntegerField(blank=True, null=True)
    rir = models.IntegerField(blank=True, null=True)
    created_at = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = "workout_sets"


class RestTimers(models.Model):
    set = models.ForeignKey(WorkoutSets, models.DO_NOTHING, blank=True, null=True)
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()

    class Meta:
        managed = False
        db_table = "rest_timers"


class WorkoutMedia(models.Model):
    session = models.ForeignKey(WorkoutSessions, models.DO_NOTHING, blank=True, null=True)
    exercise = models.ForeignKey(Exercises, models.DO_NOTHING, blank=True, null=True)
    file_url = models.TextField()
    uploaded_at = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = "workout_media"


class PersonalRecords(models.Model):
    user = models.ForeignKey(
        User, models.DO_NOTHING, blank=True, null=True, db_column="user_id"
    )
    exercise = models.ForeignKey(Exercises, models.DO_NOTHING, blank=True, null=True)
    weight = models.DecimalField(max_digits=6, decimal_places=2)
    reps = models.IntegerField()
    estimated_1rm = models.DecimalField(
        max_digits=6, decimal_places=2, blank=True, null=True
    )
    achieved_at = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = "personal_records"


class Measurements(models.Model):
    user = models.ForeignKey(
        User, models.DO_NOTHING, blank=True, null=True, db_column="user_id"
    )
    date = models.DateField()
    weight = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True)
    body_fat = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True)
    waist = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True)
    chest = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True)
    arms = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True)
    hips = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True)

    class Meta:
        managed = False
        db_table = "measurements"


class WorkoutTemplates(models.Model):
    user = models.ForeignKey(
        User, models.DO_NOTHING, blank=True, null=True, db_column="user_id"
    )
    name = models.CharField(max_length=255)
    created_at = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = "workout_templates"


class TemplateExercises(models.Model):
    template = models.ForeignKey(WorkoutTemplates, models.DO_NOTHING, blank=True, null=True)
    exercise = models.ForeignKey(Exercises, models.DO_NOTHING, blank=True, null=True)
    target_sets = models.IntegerField(blank=True, null=True)
    target_reps = models.IntegerField(blank=True, null=True)
    position = models.IntegerField()

    class Meta:
        managed = False
        db_table = "template_exercises"


class ProgressionRules(models.Model):
    exercise = models.ForeignKey(Exercises, models.DO_NOTHING, blank=True, null=True)
    increment_weight = models.DecimalField(
        max_digits=5, decimal_places=2, blank=True, null=True
    )
    increment_reps = models.IntegerField(blank=True, null=True)
    notes = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = "progression_rules"


class Notifications(models.Model):
    user = models.ForeignKey(
        User, models.DO_NOTHING, blank=True, null=True, db_column="user_id"
    )
    message = models.TextField()
    send_at = models.DateTimeField()
    created_at = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = "notifications"


class UserSettings(models.Model):
    user = models.OneToOneField(
        User, models.DO_NOTHING, primary_key=True, db_column="user_id"
    )
    weight_unit = models.CharField(max_length=10, blank=True, null=True)
    distance_unit = models.CharField(max_length=10, blank=True, null=True)
    theme = models.CharField(max_length=20, blank=True, null=True)

    class Meta:
        managed = False
        db_table = "user_settings"
