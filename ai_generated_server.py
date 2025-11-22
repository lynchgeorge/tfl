from flask import Flask, render_template, jsonify, request
import requests
import os
import dotenv
from datetime import datetime, timezone

dotenv.load_dotenv()

APP_ID = os.getenv("app_id") or os.getenv("APP_ID")
APP_KEY = os.getenv("app_key") or os.getenv("APP_KEY")
TFL_BASE = "https://api.tfl.gov.uk"

app = Flask(__name__, template_folder="templates")


def _tfl_get(path, params=None):
    params = params.copy() if params else {}
    if APP_ID:
        params.setdefault("app_id", APP_ID)
    if APP_KEY:
        params.setdefault("app_key", APP_KEY)
    url = f"{TFL_BASE}{path}"
    r = requests.get(url, params=params, timeout=10)
    r.raise_for_status()
    return r.json()


@app.route("/positions")
def positions():
    """
    Query arrivals and stop points for requested lines and return a JSON list of
    train positions (one item per predicted arrival). Query param: lines=central,victoria
    """
    lines_param = request.args.get("lines", "victoria,central,circle,elizebeth,jubilee,bakerloo,district")
    lines = [l.strip() for l in lines_param.split(",") if l.strip()]
    results = []

    for line in lines:
        try:
            # get stop points for this line -> map naptanId to lat/lon
            stoppoints = _tfl_get(f"/Line/{line}/StopPoints")
            sp_map = {sp.get("naptanId"): {"lat": sp.get("lat"), "lon": sp.get("lon"), "commonName": sp.get("commonName")} for sp in stoppoints}

            # get arrivals for this line
            arrivals = _tfl_get(f"/Line/{line}/Arrivals")
            for a in arrivals:
                naptan = a.get("naptanId")
                coords = sp_map.get(naptan)
                if not coords:
                    # skip arrivals without geo info
                    continue
                # build a compact record
                expected_iso = a.get("expectedArrival")  # ISO string from TfL
                # convert timeToStation to seconds if present
                tts = a.get("timeToStation")
                results.append({
                    "lineId": a.get("lineId"),
                    "platformName": a.get("platformName"),
                    "destinationName": a.get("destinationName"),
                    "expectedArrival": expected_iso,
                    "timeToStation": tts,
                    "naptanId": naptan,
                    "stationName": coords.get("commonName"),
                    "lat": coords.get("lat"),
                    "lon": coords.get("lon"),
                    "modeName": a.get("modeName"),
                })
        except Exception as e:
            # don't break entire response if one line fails; include an error entry
            results.append({"error": str(e), "lineId": line})

    # Optionally sort by timeToStation ascending
    results = sorted([r for r in results if "error" not in r], key=lambda x: (x.get("timeToStation") or 999999))
    # Append any error entries at end
    error_entries = [r for r in results if "error" in r]
    response = results + error_entries
    return jsonify(response)


@app.route("/")
def index():
    # default lines shown on the map can be configured via query param "lines"
    return render_template("index.html")


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)
