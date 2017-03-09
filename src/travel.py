from googlemaps.exceptions import TransportError, Timeout
from src.exceptions import ImpossibleTravel, TooManyWaypoints, NoStationInArea
from settings import gmaps
from src.location import Location
from src.car import Car


class Travel:
    def __init__(self, origin, destination, stations_list, **kwargs):
        # Optional parameters initialisation
        self.battery_lowest = kwargs.get('battery_lowest', 15)
        self.station_max_distance = kwargs.get('station_max_distance', 20000)
        self.car = kwargs.get('car', Car('default', 50, 35))

        # Primary data: origin and destination locations, and charging station list
        self.origin = origin
        self.destination = destination
        self.stations_list = stations_list

        self.distance = 0
        self.duration = 0
        self.steps = []

        # Become an array if the travel need to stop at some charging station.
        self.waypoints = None
        self.stations = []

        self.get_direct_road()
        self.find_empty_battery_location()

    def get_direct_road(self):
        """
        Get the direct road from the origin to the destination. Without stopping at any waypoints/station.
        Store the distance, the duration and the step of the travel. With Google Map API Directions.
        """
        try:
            direction = gmaps.directions('place_id:' + self.origin.key, 'place_id:' + self.destination.key)
        except (TransportError, Timeout):
            raise ImpossibleTravel('The requested travel is impossible by car.')
        else:
            self.distance = direction[0]['legs'][0]['distance']['value']
            self.duration = direction[0]['legs'][0]['duration']['value']

            for step in direction[0]['legs'][0]['steps']:
                step_data = {'distance': step['distance']['value'],
                             'duration': step['duration']['value'],
                             'start_location': {'lat': step['start_location']['lat'],
                                                'lng': step['start_location']['lng']}
                             }
                self.steps.append(step_data)

    # TODO: recuperer les coordonnee (lat et lng) d'une station, dans la base de donnee, depuis son ID.
    def get_road_with_stations(self):
        waypoints = []
        for station in self.stations:
            coords = ''  # TODO: recuperer coord station depuis ddb.

    def find_empty_battery_location(self):
        """
        Use the direct road's data and the car's data to find where the battery will be out of energy.
        """
        distance_max = int(self.car.math_distance_max(self.battery_lowest))

        if distance_max <= self.distance:
            self.waypoints = []
            waypoints_amount = 0
            distance = 0

            for step in self.steps:
                if distance_max < distance + step['distance']:
                    if waypoints_amount >= 23:
                        raise TooManyWaypoints(
                            'This travel is too long A travel can not stop at more than 23 stations.')
                    else:
                        self.waypoints.append(step['start_location'])
                        waypoints_amount += 1
                        distance = 0
                else:
                    distance += step['distance']
            print self.waypoints

    # TODO: Fonction non verifiee. Fonctionne en theorie.
    # TODO: Cette fonction utilise stations_list. Trouver structure de donnee pour station_list.
    def get_nearest_station_from_waypoints(self):
        """
        For each waypoints, retrieve the id of the nearest charging station. And store it into
        'self.stations' array.
        """
        if self.waypoints is not None:
            for location in self.waypoints:
                station = Location(lat=location['lat'],
                                   lng=location['lng']).get_nearest_station(self.stations_list,
                                                                            self.station_max_distance)
                if station:
                    self.stations.append(station[0])
                else:
                    raise NoStationInArea("There's no charging station in the area of this location",
                                          location['lat'], location['lng'])


# car = Car('bmw', 100, 25)
station_list = None
way = Travel(Location(address="SNCB Mons Station"), Location(lat=51.2142821, lng=2.9207283), station_list)
print way.destination.address
# print way.steps
