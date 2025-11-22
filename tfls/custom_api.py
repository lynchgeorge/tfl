import requests
import os
import dotenv

dotenv.load_dotenv()

APP_ID = os.getenv("app_id")
APP_KEY = os.getenv("app_key")
TFL_BASE = "https://api.tfl.gov.uk"

def tfl_get(path: str, extra_params: dict = None) -> object:
    """
    Call the TfL API directly on the given path, e.g.
    '/Line/{lineName}/StopPoints' and the given extra query parameters.
    Return a Python object corresponding to the JSON returned or raise if
    unsuccessful.
    """
    params = extra_params.copy() if extra_params else {}
    if APP_ID:
        params.setdefault("app_id", APP_ID)
    if APP_KEY:
        params.setdefault("app_key", APP_KEY)
    url = f"{TFL_BASE}{path}"
    r = requests.get(url, params=params, timeout=10)
    r.raise_for_status()
    return r.json()

if __name__ == "__main__":
    print(tfl_get(f"/Line/victoria/StopPoints"))
