"""
Very bad very simple UI that repeatedly gets all live trains, creates a static
HTML file in /tmp that plots all their current locations on OpenStreetMap
coloured according to their line's colour, and opens that HTML file in the
browser.
"""

import tfls

while True:
    trains = tfls.get_trains()
    tfls.plot_points(map(lambda train: (train.lat, train.long), trains), line_ids=map(lambda train: train.line, trains))
