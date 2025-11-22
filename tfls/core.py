from tfls.custom_api import tfl_get


MODES = [
    #'bus',
    #'cable-car',
    #'coach',
    #'cycle',
    #'cycle-hire',
    #'dlr',
    'elizabeth-line',
    #'interchange-keep-sitting',
    #'interchange-secure',
    #'national-rail',
    #'overground',
    #'replacement-bus',
    #'river-bus',
    #'river-tour',
    #'taxi',
    #'tram',
    'tube',
    #'walking'
]

def verify():
    return 'tfls is working!'


def get_line_ids():
    return [line["name"] for mode in MODES for line in tfl_get(f"/Line/Mode/{mode}")]
