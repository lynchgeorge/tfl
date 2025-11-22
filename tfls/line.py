from copy import deepcopy
from tfls.core import get_line_ids
from tfls.station import *


class Line:
    def __init__(self, line_id: str, list_of_stations: list[Station]):
        self.line_id = line_id
        self.stations = deepcopy(list_of_stations)

    def __str__(self):
        return f'{self.line_id} Line, consisting of {len(self.stations)} stations'

    def __repr__(self):
        return self.__str__()

    def __eq__(self, other):
        return  repr(self) == repr(other)

    def __iter__(self):
        for station in self.stations:
            yield station

    def get_station(self, station_name):
        '''
        Iterates through the list of stations on the line,
        and returns the first station for which is_station
        is true.
        '''
        for station in self.stations:
            if station.is_station(station_name):
                return station


def get_line_by_id(client, line_id):
    stations = get_stations_on_line(client, line_id)
    return Line(line_id, stations)


def get_lines(client):
    line_ids = get_line_ids()
    return [get_line_by_id(client, line_id)
            for line_id in line_ids]
