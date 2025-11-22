

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


def stoppoint_to_station(stop_point, line_id):
    '''
    Convert StopPoint to Stations.
    '''
    stop_point_dict = stop_point.as_dict()
    name = stop_point_dict['common_name']
    id = stop_point_dict['id']
    lat = stop_point_dict['lat']
    lon = stop_point_dict['lon']

    return Station(id, name, lat, lon, line_id)


def get_stations_on_line(client, line_id):
    stations_on_line = client.get_stop_points_by_line_id(line_id)
    return [stoppoint_to_station(stop_point, line_id)
            for stop_point in stations_on_line]

