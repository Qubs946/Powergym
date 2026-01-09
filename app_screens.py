from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.properties import ObjectProperty, BooleanProperty
from kivy.logger import Logger
from kivymd.toast import toast
from api_client import login, get_exercises, register, create_exercise
from kivymd.uix.dialog import MDDialog
from kivymd.uix.button import MDFlatButton, MDRaisedButton
from kivymd.uix.textfield import MDTextField

from kivymd.uix.list import OneLineListItem


# Klasy zarządzające ekranami (widoki)
# Nie dodajemy tu żadnego kodu wizualnego, tylko logikę,
# a wygląd definiujemy w design.kv.

class RootScreenManager(ScreenManager):
    """
    Główny menedżer ekranów aplikacji.
    Definiuje, które ekrany są dostępne.
    """
    pass # Logika przełączania będzie zdefiniowana w design.kv lub dodana tu później.

class RejestracjaScreen(Screen):
    """
    Ekran Rejestracji (iPhone Rejestracja).
    """

    def do_register(self):
        print("REGISTER IDS:", list(self.ids.keys()))
        Logger.info("REGISTER: do_register() fired")
        print("REGISTER: do_register() fired")
        email = self.ids.email_reg.text.strip()
        password = self.ids.password_reg.text.strip()
        confirm = self.ids.confirm_password_reg.text.strip()

        if not email or not password:
            self.ids.register_status.text = "Podaj email i hasło."
            return

        if password != confirm:
            self.ids.register_status.text = "Hasła nie są takie same."
            return

        ok, msg = register(email, password)
        self.ids.register_status.text = msg

        if ok:
            self.manager.current = "logowanie"

    pass

class LogowanieScreen(Screen):
    """
    Ekran Logowania (iPhone Logowanie).
    """

    def do_login(self):
        email = self.ids.email_login.text.strip()
        password = self.ids.password_login.text

        ok = login(email, password)
        if ok:
            self.manager.current = "menu_glowne"
        else:
            # jeśli masz labelkę na komunikaty:
            if "login_status" in self.ids:
                self.ids.login_status.text = "Błędny login lub hasło"
            print("LOGIN FAILED")

    pass

class MenuGlowneScreen(Screen):
    """
    Ekran Menu Głównego (iPhone Menu Główne).
    """

    def on_enter(self):
        try:
            exercises = get_exercises()
            print("HOME: exercises count =", len(exercises))
        except Exception as e:
            print("HOME ERROR:", e)

    pass

class TreningScreen(Screen):
    """
    Ekran Wyboru Treningu (iPhone Trening, iPhone 16 Pro - 17).
    """
    # BooleanProperty automatycznie aktualizuje UI gdy wartość się zmienia
    routines_expanded = BooleanProperty(True)  # Domyślnie rozwinięte

    def toggle_routines_visibility(self):
        """
        Przełącza widoczność listy rutyn treningowych.
        Zmienia ikonę chevron i pokazuje/ukrywa ScrollView z kartami treningowymi.

        Właściwości ScrollView (height, opacity, disabled) są bindowane bezpośrednio
        w pliku .kv do wartości routines_expanded, więc wystarczy zmienić tę wartość.
        """
        # Przełącz stan - wszystkie zmiany UI następują automatycznie przez property binding
        self.routines_expanded = not self.routines_expanded

class ProfileScreen(Screen):
    """
    Ekran profilu użytkownika.
    """
    pass


class ActiveRoutineScreen(Screen):
    """
    Ekran aktywnego treningu.
    Pokazuje timer, listę ćwiczeń, logowanie serii.
    """
    pass


class WorkoutSummaryScreen(Screen):
    """
    Ekran podsumowania treningu (wyświetlany po zakończeniu).
    Pokazuje: czas treningu, volume, liczba serii, pobite rekordy (PRs),
    statystyki grup mięśniowych, opcję zapisu/anulowania.

    Wzorowany na Hevy - workout summary po kliknięciu "Finish".
    """
    pass


class WorkoutHistoryScreen(Screen):
    """
    Ekran historii treningów.
    Wyświetla kalendarz/listę wszystkich wykonanych treningów.
    Umożliwia filtrowanie i przeglądanie szczegółów.

    Wzorowany na Hevy - zakładka z historią wszystkich sesji.
    """
    pass


class ExerciseLibraryScreen(Screen):
    """
    Ekran biblioteki ćwiczeń.
    Wyświetla 400+ ćwiczeń z możliwością filtrowania po:
    - Grupach mięśniowych (Back, Chest, Legs, Arms, Shoulders, Core)
    - Wyposażeniu (Barbell, Dumbbell, Machine, Bodyweight, Cable, etc.)
    - Typie (Strength, Cardio, Stretching)

    Wzorowany na Hevy Exercise Library.
    Zawiera search bar i kategorie filtrów.
    """

    add_dialog = None

    def on_enter(self):
        self.refresh_list()

    def refresh_list(self):
        if "exercise_library_list" not in self.ids:
            print("Brak id: exercise_library_list w KV")
            return

        container = self.ids.exercise_library_list
        container.clear_widgets()

        try:
            exercises = get_exercises()
        except Exception as e:
            toast(f"Błąd pobierania: {e}")
            return

        if not exercises:
            container.add_widget(OneLineListItem(text="Brak ćwiczeń. Dodaj pierwsze +"))
            return

        for ex in exercises:
            container.add_widget(OneLineListItem(text=ex.get("name", "Bez nazwy")))

    def open_add_exercise_dialog(self):
        # Tworzymy dialog tylko raz
        if not self.add_dialog:
            self._name_field = MDTextField(
                hint_text="Nazwa ćwiczenia",
                mode="rectangle",
            )
            self._cat_field = MDTextField(
                hint_text="Kategoria (opcjonalnie)",
                mode="rectangle",
            )
            self._desc_field = MDTextField(
                hint_text="Opis (opcjonalnie)",
                mode="rectangle",
                multiline=True,
            )

            self.add_dialog = MDDialog(
                title="Dodaj ćwiczenie",
                type="custom",
                content_cls=self._build_dialog_content(),
                buttons=[
                    MDFlatButton(text="Anuluj", on_release=lambda x: self.add_dialog.dismiss()),
                    MDRaisedButton(text="Dodaj", on_release=self._submit_exercise),
                ],
            )

        # Czyścimy pola przy każdym otwarciu
        self._name_field.text = ""
        self._cat_field.text = ""
        self._desc_field.text = ""
        self.add_dialog.open()

    def _build_dialog_content(self):
        # prosta kolumna z polami
        from kivy.uix.boxlayout import BoxLayout
        box = BoxLayout(orientation="vertical", spacing="12dp", size_hint_y=None)
        box.bind(minimum_height=box.setter("height"))
        box.add_widget(self._name_field)
        box.add_widget(self._cat_field)
        box.add_widget(self._desc_field)
        return box

    def _submit_exercise(self, *args):
        name = self._name_field.text.strip()
        category = self._cat_field.text.strip()
        description = self._desc_field.text.strip()

        if not name:
            toast("Podaj nazwę ćwiczenia.")
            return

        try:
            create_exercise(name=name, category=category or None, description=description or None)
        except Exception as e:
            toast(f"Nie udało się dodać: {e}")
            return

        toast("Dodano ćwiczenie!")
        self.add_dialog.dismiss()
        self.refresh_list()

    def add_exercise(self):

        name = self.ids.new_ex_name.text.strip()
        category = self.ids.new_ex_category.text.strip()
        desc = self.ids.new_ex_desc.text.strip()

        if not name:
            toast("Podaj nazwę ćwiczenia.")
            return

        try:
            add_exercise(name=name, category=category, description=desc)
            toast("Dodano ćwiczenie!")
        except Exception as e:
            toast(f"Nie udało się dodać: {e}")
            return

        self.ids.new_ex_name.text = ""
        self.ids.new_ex_category.text = ""
        self.ids.new_ex_desc.text = ""

        self.refresh_list()
    pass


class ExerciseDetailScreen(Screen):
    """
    Ekran szczegółów pojedynczego ćwiczenia.
    Pokazuje:
    - Nazwę i alias ćwiczenia
    - GIF/wideo instruktażowe (placeholder)
    - Opis wykonania
    - Zaangażowane grupy mięśniowe (primary, secondary)
    - Wymagane wyposażenie
    - Historię wykonania (jeśli ćwiczenie było logowane)
    - Wykresy postępów
    - Przycisk "Add to Routine"

    Wzorowany na Hevy Exercise Detail View.
    """
    pass


class RoutineBuilderScreen(Screen):
    """
    Ekran tworzenia/edycji rutyny treningowej.
    Umożliwia:
    - Nazwanie rutyny
    - Dodawanie ćwiczeń z biblioteki
    - Ustawianie docelowej liczby serii i powtórzeń
    - Organizację ćwiczeń w kolejności
    - Grupowanie w supersets
    - Zapisywanie rutyny do folderu

    Wzorowany na Hevy Routine Builder.
    """
    pass


class ExerciseAnalyticsScreen(Screen):
    """
    Ekran analizy postępów dla pojedynczego ćwiczenia.
    Pokazuje:
    - Wykres wagi × czas (line chart)
    - Wykres volume × czas
    - Tabela wszystkich wykonanych serii
    - Personal Records (1RM, 3RM, 5RM, etc.)
    - Statystyki (avg weight, avg reps, total sets)

    Wzorowany na Hevy Exercise Performance View.
    """
    pass


class BodyMeasurementsScreen(Screen):
    """
    Ekran pomiarów ciała.
    Pokazuje:
    - Lista pomiarów (Weight, Body Fat %, Chest, Waist, etc.)
    - Wykresy trendów dla każdego pomiaru
    - Możliwość dodania nowego pomiaru
    - Historia pomiarów

    Wzorowany na Hevy Body Measurements.
    """
    pass


class ProgressPhotosScreen(Screen):
    """
    Ekran galerii zdjęć postępów.
    Pokazuje:
    - Grid zdjęć progress photos
    - Możliwość dodania nowego zdjęcia
    - Porównanie przed/po
    - Timeline zdjęć

    Wzorowany na Hevy Progress Photos.
    """
    pass


class SettingsScreen(Screen):
    """
    Ekran ustawień aplikacji.
    Opcje:
    - Units (kg/lbs, cm/in)
    - Default rest timer
    - Theme (Dark/Light)
    - Notifications
    - Account settings
    - Export/Import data
    - About

    Wzorowany na Hevy Settings.
    """
    pass


class WorkoutTemplatesScreen(Screen):
    """
    Ekran gotowych planów treningowych (templates).
    Pokazuje predefiniowane plany jak:
    - 3X/WEEK FULL BODY
    - PUSH/PULL Split
    - 4X/WEEK UPPER/LOWER
    - 5X/WEEK PUSH/PULL/LEGS

    Każdy plan zawiera:
    - Obrazek reprezentujący plan
    - Nazwę planu
    - Opis (częstotliwość, split)
    - Przypisane ćwiczenia
    - Przycisk do rozpoczęcia planu

    Wzorowany na mockup PowerGym.
    """
    pass
