from flask import Flask, render_template, jsonify
import folium
import sys
import os

# Add the parent directory to the Python path to access tfls
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..")))

from tfls.line import get_lines
from tfls.custom_api import tfl_get

app = Flask(__name__, static_folder="static", template_folder="templates")

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/map")
def map_view():
    # Create a folium map centered on London
    london_map = folium.Map(location=[51.5074, -0.1278], zoom_start=12)

    # Revert to predefined static colors for tube lines
    line_colors = {
        'victoria': 'blue',
        'central': 'red',
        'northern': 'black',
        'bakerloo': 'brown',
        'piccadilly': 'darkblue',
        'dlr': 'turquoise',
        'metropolitan': 'purple',
        'jubilee': 'silver',
        'circle': 'yellow',
        'district': 'green'
    }

    # Fetch all lines and their stations
    lines = get_lines()
    for line in lines:
        color = line_colors.get(line.line_id, 'blue')  # Default to blue if no color is defined

        # Sort stations by their order in the line
        stations_sorted = sorted(line.stations, key=lambda station: station.id)
        coordinates = [[station.lat, station.lon] for station in stations_sorted]

        for station in stations_sorted:
            folium.Marker(
                location=[station.lat, station.lon],
                popup=f"{station.name} ({line.line_id})",
                icon=folium.Icon(color=color, icon="info-sign")
            ).add_to(london_map)

        # Add a polyline for the tube line
        folium.PolyLine(
            locations=coordinates,
            color=color,
            weight=5,
            opacity=0.8
        ).add_to(london_map)

    # Save the map to an HTML file
    map_path = os.path.join(os.path.dirname(__file__), "templates", "map.html")
    london_map.save(map_path)
    return render_template("map.html")

if __name__ == "__main__":
    app.run(debug=True)
