from kivymd.app import MDApp
from kivy.lang import Builder
from kivy.properties import ObjectProperty
from app_screens import RootScreenManager
from ui_widgets import WorkoutCard
import os
from kivy.core.window import Window
#from kivymd.tools.hotreload.app import MDApp

import requests

BASE_URL = "http://127.0.0.1:8000"
TOKEN = None

# Wskazówka: Ustawienie PATH do katalogu z plikiem .kv.
# Zapewnia, że Kivy znajdzie design.kv, jeśli nazwa klasy głównej 
# nie pasuje do nazwy pliku .kv (tutaj pasuje, ale to dobra praktyka).
Builder.load_file(os.path.join(os.path.dirname(__file__), 'design.kv'))



class PowerGymApp(MDApp):
    """
    Główna klasa aplikacji PowerGym.
    """
    # Używamy RootScreenManager zdefiniowanego w app_screens.py
    # aby zarządzać przełączaniem ekranów.
    # Wskazówka: Zawsze używaj właściwości, jeśli chcesz, aby widżet był
    # dostępny poza metodą build() lub jeśli ma reagować na zmiany.
    Window.size = (375, 750)
    root_manager = ObjectProperty(None)


    def build(self):
        """
        Inicjalizuje i zwraca główny interfejs użytkownika.
        """
        self.theme_cls.primary_palette = "Green"  # Główny kolor aplikacji
        self.theme_cls.accent_palette = "Teal"  # Kolor akcentujący
        self.theme_cls.theme_style = "Dark"  # Używamy ciemnego motywu

        # Tworzymy instancję głównego menedżera ekranów, 
        # który jest zdefiniowany w design.kv
        self.root_manager = RootScreenManager()
        return self.root_manager

    def on_start(self):
        """
        Wywoływane po starcie aplikacji.
        """
        print("Aplikacja PowerGym wystartowała.")



# USTAWIENIA ROZMIARU OKNA (SYMULACJA TELEFONU)
# Wskazówka: Szerokość 375 i Wysokość 667 to standardowe wymiary iPhone 6/7/8
WINDOW_WIDTH = 375
WINDOW_HEIGHT = 667

# Ustawienie stałego rozmiaru okna
Window.size = (WINDOW_WIDTH, WINDOW_HEIGHT)

# Dodatkowa wskazówka: Jeśli nie chcesz, aby użytkownik mógł zmieniać rozmiar,
# możesz zablokować skalowanie (unikanie błędów podczas pracy z układem):
Window.resizable = False


def login(username, password):
    global TOKEN
    url = f"{BASE_URL}/api/auth/token/"
    response = requests.post(
        url,
        data={
            "username": username,
            "password": password
        }
    )

    if response.status_code == 200:
        TOKEN = response.json()["access"]
        return True
    else:
        return False


def auth_headers():
    if not TOKEN:
        return {}
    return {
        "Authorization": f"Bearer {TOKEN}"
    }


def get_exercises():
    url = f"{BASE_URL}/api/exercises/"
    response = requests.get(url, headers=auth_headers())
    return response.json()


def create_workout_session(plan_day_id=None):
    url = f"{BASE_URL}/api/workout-sessions/"
    data = {
        "plan_day": plan_day_id
    }
    response = requests.post(url, json=data, headers=auth_headers())
    return response.json()

if __name__ == '__main__':
    PowerGymApp().run()