import requests

BASE_URL = "http://127.0.0.1:8000"
TOKEN = None


def login(username: str, password: str) -> bool:
    global TOKEN
    url = f"{BASE_URL}/api/auth/token/"
    r = requests.post(url, json={"username": username, "password": password}, timeout=10)

    print("LOGIN STATUS:", r.status_code)
    print("LOGIN BODY:", r.text)

    if r.status_code == 200:
        TOKEN = r.json().get("access")
        return TOKEN is not None
    return False


def auth_headers() -> dict:
    if not TOKEN:
        return {}
    return {"Authorization": f"Bearer {TOKEN}"}


def get_exercises():
    url = f"{BASE_URL}/api/exercises/"
    r = requests.get(url, headers=auth_headers(), timeout=10)

    print("EXERCISES STATUS:", r.status_code)
    print("EXERCISES BODY:", r.text)

    if r.status_code != 200:
        return []
    return r.json()

def register(email: str, password: str) -> tuple[bool, str]:
    url = f"{BASE_URL}/api/auth/register/"
    print("REGISTER URL:", url)
    print("REGISTER DATA:", {"email": email, "password": password})

    try:
        r = requests.post(url, json={"email": email, "password": password}, timeout=10)
    except Exception as e:
        print("REGISTER EXCEPTION:", e)
        return False, f"Wyjątek: {e}"

    print("REGISTER STATUS:", r.status_code)
    print("REGISTER BODY:", r.text)

    if r.status_code == 201:
        return True, "Konto utworzone"

    return False, r.text or "Błąd rejestracji"

def create_exercise(name: str, category: str | None = None, description: str | None = None):

    url = f"{BASE_URL}/api/exercises/"
    payload = {"name": name}
    if category:
        payload["category"] = category
    if description:
        payload["description"] = description

    r = requests.post(url, json=payload, headers=auth_headers(), timeout=10)

    print("CREATE EXERCISE STATUS:", r.status_code)
    print("CREATE EXERCISE BODY:", r.text)

    if r.status_code not in (200, 201):
        return False, r.text or "Błąd dodawania ćwiczenia"
    return True, "Ćwiczenie dodane"

def add_exercise(name, category=None, description=None, video_url=None):
    payload = {
        "name": name,
        "category": category,
        "description": description,
        "video_url": video_url,
    }
    # usuń puste pola
    payload = {k: v for k, v in payload.items() if v not in (None, "", " ")}

    r = requests.post(
        f"{BASE_URL}/api/exercises/",
        json=payload,
        headers=get_headers(),
        timeout=10,
    )
    # debug
    print("ADD EXERCISE STATUS:", r.status_code)
    print("ADD EXERCISE BODY:", r.text)

    r.raise_for_status()
    return r.json()

def get_plans():
    r = requests.get(f"{BASE_URL}/api/plans/", headers=auth_headers(), timeout=10)
    r.raise_for_status()
    return r.json()

def create_plan(name: str):
    r = requests.post(f"{BASE_URL}/api/plans/", json={"name": name}, headers=auth_headers(), timeout=10)
    r.raise_for_status()
    return r.json()

def get_plan_days(plan_id: int):
    r = requests.get(f"{BASE_URL}/api/plans/{plan_id}/days/", headers=auth_headers(), timeout=10)
    r.raise_for_status()
    return r.json()

def add_plan_day(plan_id: int, day_name: str):
    r = requests.post(f"{BASE_URL}/api/plans/{plan_id}/days/", json={"day_name": day_name}, headers=auth_headers(), timeout=10)
    r.raise_for_status()
    return r.json()

def get_plan_day_exercises(plan_day_id: int):
    r = requests.get(f"{BASE_URL}/api/plan-days/{plan_day_id}/exercises/", headers=auth_headers(), timeout=10)
    r.raise_for_status()
    return r.json()

def add_exercise_to_day(plan_day_id: int, exercise_id: int, target_sets=None, target_reps=None):
    payload = {"exercise_id": exercise_id}
    if target_sets is not None:
        payload["target_sets"] = target_sets
    if target_reps is not None:
        payload["target_reps"] = target_reps
    r = requests.post(f"{BASE_URL}/api/plan-days/{plan_day_id}/exercises/", json=payload, headers=auth_headers(), timeout=10)
    r.raise_for_status()
    return r.json()