from tfls.custom_api import tfl_get


class Station:
    def __init__(self, id, name, lat, lon, line):
        self.id = id
        self.name = name.lower()
        self.lat = lat
        self.lon = lon
        self.lines = [line]

    def __str__(self):
        return f'{self.name} ({self.lat}, {self.lon})'

    def __repr__(self):
        return self.__str__()

    def is_station(self, station_name):
        '''
        Evaluates to true if the provided
        station name is a subset of the station's
        name attribute.
        '''
        return station_name in self.name


def stoppoint_to_station(stop_point: dict, line_id: str):
    '''
    Convert StopPoint to Stations.
    '''
    name = stop_point['commonName']
    id = stop_point['id']
    lat = stop_point['lat']
    lon = stop_point['lon']

    return Station(id, name, lat, lon, line_id)


def get_stations_on_line(line_id: str):
    stations_on_line = tfl_get(f"/Line/{line_id}/StopPoints")
    return [stoppoint_to_station(stop_point, line_id)
            for stop_point in stations_on_line]
