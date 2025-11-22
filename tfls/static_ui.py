import json, tempfile, webbrowser, os
from pathlib import Path

def plot_points(coords, center=None, zoom=12, popup_texts=None, line_ids=None, map_filename=None, open_in_browser=True):
    """
    Plot a list of (lat, lon) tuples on an OpenStreetMap (Leaflet) page and open it in the browser.
    - coords: iterable of (lat, lon)
    - line_ids: optional iterable of line id strings (same length as coords) used to pick marker colours
    """

    # coords = list(filter(lambda coord: coord != (0, 0), coords))
    coords = [c for c in coords if c != (0,0)]

    # compute center if not provided
    if center is None:
        avg_lat = sum(c[0] for c in coords) / len(coords)
        avg_lon = sum(c[1] for c in coords) / len(coords)
        center = (avg_lat, avg_lon)

    # Known TfL line colours (approximate); keys lowercased for lookup
    line_color_map = {
        "bakerloo": "#B36305",
        "central": "#E32017",
        "circle": "#FFD300",
        "district": "#00782A",
        "hammersmithandcity": "#F3A9BB",
        "hammersmith & city": "#F3A9BB",
        "jubilee": "#6A7278",
        "metropolitan": "#9B0056",
        "northern": "#000000",
        "piccadilly": "#0019A8",
        "victoria": "#00A0E2",
        "waterloo&city": "#95CDBA",
        "waterloo & city": "#95CDBA",
        "overground": "#EE7C0E",
        "dlr": "#00A4A7",
        "tram": "#84B817",
        "elizabeth": "#6960A5",
        "tflrail": "#0019A8"
    }
    default_color = "#000000"

    line_ids = list(line_ids) if line_ids is not None else [None] * len(coords)

    points = []
    for i, (lat, lon) in enumerate(coords):
        col = default_color
        lid = None
        try:
            lid = line_ids[i]
        except Exception:
            lid = None
        if lid:
            col = line_color_map.get(str(lid).strip().lower(), default_color)
        pt = {"lat": float(lat), "lon": float(lon), "color": col}
        if popup_texts:
            try:
                pt["popup"] = popup_texts[i]
            except Exception:
                pt["popup"] = ""
        points.append(pt)

    # Escape JS template braces; use p.color in JS for marker colour
    template = """<!doctype html>
<html>
<head>
<meta charset="utf-8"/>
<meta name="viewport" content="width=device-width,initial-scale=1" />
<title>Map</title>
<link rel="stylesheet" href="https://unpkg.com/leaflet@1.9.4/dist/leaflet.css"/>
<style>html,body,#map{{height:100%;margin:0;padding:0}}</style>
</head>
<body>
<div id="map"></div>
<script src="https://unpkg.com/leaflet@1.9.4/dist/leaflet.js"></script>
<script>
const center = [{center_lat}, {center_lon}];
const points = {points_json};

const map = L.map('map').setView(center, {zoom});
L.tileLayer('https://{{s}}.tile.openstreetmap.org/{{z}}/{{x}}/{{y}}.png', {{
    maxZoom: 19,
    attribution: '© OpenStreetMap contributors'
}}).addTo(map);

points.forEach(p => {{
    const m = L.circleMarker([p.lat, p.lon], {{
        radius:6, color: (p.color || '{default_color}'), fillOpacity:0.9
    }});
    if (p.popup) m.bindPopup(p.popup);
    m.addTo(map);
}});
</script>
</body>
</html>""".format(
        center_lat=center[0], center_lon=center[1],
        points_json=json.dumps(points),
        zoom=int(zoom),
        default_color=default_color
    )

    print(len(points))

    # write file
    if map_filename:
        out_path = os.path.abspath(map_filename)
        with open(out_path, "w", encoding="utf-8") as f:
            f.write(template)
    else:
        fd, out_path = tempfile.mkstemp(suffix=".html", prefix="tfl_map_")
        os.close(fd)
        with open(out_path, "w", encoding="utf-8") as f:
            f.write(template)

    if open_in_browser:
        try:
            webbrowser.open(Path(out_path).as_uri())
        except Exception:
            webbrowser.open("file://" + out_path)
    return out_path
