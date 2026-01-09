from kivy.uix.boxlayout import BoxLayout
from kivy.properties import StringProperty, ListProperty, ObjectProperty, NumericProperty, BooleanProperty
from kivy.uix.behaviors import ButtonBehavior
from kivy.app import App
from kivymd.uix.card import MDCard
from kivymd.uix.label import MDLabel
from kivymd.uix.button import MDRaisedButton, MDIconButton, MDFlatButton
from kivymd.uix.list import OneLineListItem
from kivy.clock import Clock


class NavButton(ButtonBehavior, BoxLayout):
    text = StringProperty("")
    icon_source = StringProperty("")
    screen_name = StringProperty("")

    def on_release(self):
        app = App.get_running_app()
        app.root.current = self.screen_name


class BottomNavBar(BoxLayout):
    pass


class ExerciseWidget(MDCard):
    exercise_name = StringProperty("")
    sets = StringProperty("")
    reps = StringProperty("")
    weight = StringProperty("")


class NewExerciseWidget(MDCard):
    pass


class WorkoutCard(MDCard):
    title = StringProperty("")
    exercises = ListProperty([])
    app = ObjectProperty()

class ActiveExerciseWidget(MDCard):
    exercise_name = StringProperty("")
    
class ExerciseSetWidget(BoxLayout):
    set_number = StringProperty("")
    previous = StringProperty("")
    kg = StringProperty("")
    reps = StringProperty("")


# --- Nowe widgety dla Active Routine Screen (wzorowane na Hevy) ---

class WorkoutTimerWidget(BoxLayout):
    """
    Widget wyświetlający timer treningu i timer odpoczynku.
    Pokazuje czas trwania treningu w formacie MM:SS.

    Właściwości:
    - elapsed_time: Całkowity czas treningu w sekundach
    - is_resting: Czy aktualnie trwa odpoczynek między seriami
    - rest_time: Czas odpoczynku w sekundach
    """
    elapsed_time = NumericProperty(0)  # Czas treningu w sekundach
    is_resting = BooleanProperty(False)  # Czy trwa odpoczynek
    rest_time = NumericProperty(0)  # Czas odpoczynku w sekundach

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        # Automatyczne uruchomienie timera przy starcie
        Clock.schedule_interval(self.update_timer, 1.0)

    def update_timer(self, dt):
        """Aktualizacja timera co sekundę"""
        self.elapsed_time += 1
        if self.is_resting and self.rest_time > 0:
            self.rest_time -= 1
            if self.rest_time == 0:
                self.is_resting = False

    def get_formatted_time(self):
        """Formatowanie czasu na MM:SS lub HH:MM:SS"""
        hours = int(self.elapsed_time // 3600)
        minutes = int((self.elapsed_time % 3600) // 60)
        seconds = int(self.elapsed_time % 60)

        if hours > 0:
            return f"{hours}h {minutes}m {seconds}s"
        else:
            return f"{minutes}m {seconds}s"

    def start_rest_timer(self, duration=90):
        """Rozpoczyna timer odpoczynku (domyślnie 90 sekund)"""
        self.rest_time = duration
        self.is_resting = True


class RPESelector(BoxLayout):
    """
    Widget do wyboru RPE (Rate of Perceived Exertion) - skala 1-10.
    RPE określa jak trudny był dany set (10 = maksymalne wyczerpanie).

    Właściwości:
    - selected_rpe: Wybrany poziom RPE (1-10)
    """
    selected_rpe = NumericProperty(5)  # Domyślnie RPE = 5


class SetTypeSelector(BoxLayout):
    """
    Widget do wyboru typu serii podczas treningu.

    Typy serii (wzorowane na Hevy):
    - Normal: Standardowa seria
    - Warmup: Seria rozgrzewkowa
    - Drop Set: Seria ze zmniejszeniem ciężaru
    - Failure: Seria do całkowitego wyczerpania

    Właściwości:
    - selected_type: Aktualnie wybrany typ serii
    """
    selected_type = StringProperty("Normal")  # Domyślnie "Normal"

    def set_type(self, type_name):
        """Ustawia typ serii"""
        self.selected_type = type_name


class WorkoutStatsBar(BoxLayout):
    """
    Widget wyświetlający statystyki treningu na górze ekranu.
    Pokazuje: Duration (czas), Volume (całkowity ciężar), Sets (liczba serii).

    Właściwości:
    - duration: Czas treningu (string, np. "45m 30s")
    - volume: Całkowity ciężar w kg (string, np. "2500 kg")
    - sets_count: Liczba wykonanych serii (string, np. "12")
    """
    duration = StringProperty("0m 0s")
    volume = StringProperty("0 kg")
    sets_count = StringProperty("0")


class ExerciseImagePlaceholder(BoxLayout):
    """
    Placeholder na obrazek/gif instruktażowy dla ćwiczenia.
    W przyszłości zostanie zastąpiony prawdziwymi obrazkami z backendu.

    Właściwości:
    - image_path: Ścieżka do obrazka (domyślnie placeholder)
    - exercise_name: Nazwa ćwiczenia (dla tooltipa)
    """
    image_path = StringProperty("assets/image.png")
    exercise_name = StringProperty("")


# --- Widgety dla Exercise Library (PRIORITY 2) ---

class ExerciseLibraryCard(MDCard):
    """
    Karta ćwiczenia w bibliotece.
    Wyświetla: obrazek, nazwę, grupy mięśniowe, wyposażenie, przycisk ADD.

    Właściwości:
    - exercise_name: Nazwa ćwiczenia
    - muscle_groups: Grupy mięśniowe (string, np. "Back, Biceps")
    - equipment: Wymagane wyposażenie (string, np. "Barbell")
    - image_path: Ścieżka do obrazka/GIFa
    """
    exercise_name = StringProperty("")
    muscle_groups = StringProperty("")
    equipment = StringProperty("")
    image_path = StringProperty("assets/image.png")


class FilterChipWidget(BoxLayout):
    """
    Chip do filtrowania (np. "Chest", "Barbell", "Strength").
    Używany w Exercise Library do filtrowania po kategoriach.

    Właściwości:
    - label: Tekst wyświetlany na chipie
    - is_selected: Czy chip jest aktualnie wybrany
    - category: Kategoria filtra ("muscle", "equipment", "type")
    """
    label = StringProperty("")
    is_selected = BooleanProperty(False)
    category = StringProperty("")

    def toggle_selection(self):
        """Przełącza stan wybrania chipa"""
        self.is_selected = not self.is_selected


class MuscleGroupBadge(BoxLayout):
    """
    Badge pokazujący grupę mięśniową (np. "Chest" z ikoną).
    Używany w Exercise Detail i Exercise Card.

    Właściwości:
    - muscle_name: Nazwa grupy mięśniowej
    - is_primary: Czy to główna grupa (True) czy pomocnicza (False)
    """
    muscle_name = StringProperty("")
    is_primary = BooleanProperty(True)


class RoutineExerciseItem(MDCard):
    """
    Widget reprezentujący ćwiczenie w Routine Builder.
    Pokazuje nazwę, docelowe serie/reps, możliwość drag&drop, usunięcia.

    Właściwości:
    - exercise_name: Nazwa ćwiczenia
    - target_sets: Docelowa liczba serii (string, np. "3")
    - target_reps: Docelowe powtórzenia (string, np. "8-12")
    - order_number: Numer kolejności w rutynie
    """
    exercise_name = StringProperty("")
    target_sets = StringProperty("3")
    target_reps = StringProperty("8-12")
    order_number = NumericProperty(1)


# --- Widgety dla Profile & Statistics (PRIORITY 3) ---

class StatCard(MDCard):
    """
    Karta statystyki w profilu (np. Total Workouts, Volume, PRs).
    Wyświetla ikonę, nazwę statystyki i wartość.

    Właściwości:
    - stat_name: Nazwa statystyki (string, np. "Total Workouts")
    - stat_value: Wartość (string, np. "127")
    - icon_name: Nazwa ikony Material Design
    - accent_color: Kolor akcentu (hex, domyślnie cyan)
    """
    stat_name = StringProperty("")
    stat_value = StringProperty("")
    icon_name = StringProperty("chart-line")
    accent_color = StringProperty("14B8A6")


class PersonalRecordCard(MDCard):
    """
    Karta Personal Record (rekord osobisty).
    Pokazuje ćwiczenie, wartość PR i datę ustanowienia.

    Właściwości:
    - exercise_name: Nazwa ćwiczenia
    - pr_value: Wartość PR (string, np. "100kg x 5")
    - date_achieved: Data ustanowienia (string, np. "Dec 27, 2025")
    """
    exercise_name = StringProperty("")
    pr_value = StringProperty("")
    date_achieved = StringProperty("")


class StreakWidget(BoxLayout):
    """
    Widget pokazujący streak (dni z rzędu treningów).
    Wyświetla ikonę ognia i licznik.

    Właściwości:
    - streak_days: Liczba dni z rzędu (int)
    - is_active: Czy streak jest aktywny (dzisiaj był trening)
    """
    streak_days = NumericProperty(0)
    is_active = BooleanProperty(True)


class WeeklyActivityWidget(BoxLayout):
    """
    Widget pokazujący aktywność w danym tygodniu (kafelki dni).
    Wzorowany na GitHub contribution graph.

    Właściwości:
    - week_data: Lista 7 wartości boolean (czy był trening w dany dzień)
    """
    week_data = ListProperty([False, True, True, False, True, True, False])


class BodyMeasurementItem(MDCard):
    """
    Widget pojedynczego pomiaru ciała (np. Weight, Body Fat %).
    Pokazuje nazwę, aktualną wartość, zmianę i wykres trendu.

    Właściwości:
    - measurement_name: Nazwa pomiaru (string, np. "Weight")
    - current_value: Aktualna wartość (string, np. "75.5 kg")
    - change_value: Zmiana (string, np. "-2.3 kg")
    - is_positive_change: Czy zmiana jest pozytywna (dla wagi: False)
    """
    measurement_name = StringProperty("")
    current_value = StringProperty("")
    change_value = StringProperty("")
    is_positive_change = BooleanProperty(True)


class ExercisePreviewItem(BoxLayout):
    """
    Widget pojedynczego ćwiczenia w karcie CompletedWorkoutCard.
    Pokazuje okrągły obrazek i tekst "X sets Exercise Name".
    """
    exercise_image = StringProperty("assets/image.png")
    exercise_text = StringProperty("3 sets Exercise Name")


class CompletedWorkoutCard(MDCard):
    """
    Karta zakończonego treningu w stylu Hevy.
    Pokazuje nazwę rutyny, czas, objętość i listę ćwiczeń.

    Właściwości:
    - workout_name: Nazwa treningu (string, np. "Pull A")
    - workout_time: Czas treningu (string, np. "1h 40min")
    - workout_volume: Objętość (string, np. "8 738 kg")
    - exercises_preview: Lista pierwszych 3 ćwiczeń (list)
    - hidden_exercises_count: Liczba ukrytych ćwiczeń (int)
    """
    workout_name = StringProperty("Workout Name")
    workout_time = StringProperty("0h 0min")
    workout_volume = StringProperty("0 kg")
    exercises_preview = ListProperty([])  # Lista tupli: (image_path, "3 sets Exercise Name")
    hidden_exercises_count = NumericProperty(0)