

class Station:
    def __init__(self, id, name, lat, lon):
        self.id = id
        self.name = name.lower()
        self.lines = []
        self.lat = lat
        self.lon = lon
    
    def __str__(self):
        return f'{self.name} ({self.lat}, {self.lon})'

    def __repr__(self):
        return self.__str__()


def stoppoint_to_station(stop_point):
    '''
    Convert StopPoint to Stations.
    '''
    stop_point_dict = stop_point.as_dict()
    name = stop_point_dict['common_name']
    id = stop_point_dict['id']
    lat = stop_point_dict['id']
    lon = stop_point_dict['id']

    return Station(id, name, lat, lon)


def get_stations_on_line(client, line_id):
    stations_on_line = client.get_stop_points_by_line_id(line_id)
    return [stoppoint_to_station(stop_point)
            for stop_point in stations_on_line]

