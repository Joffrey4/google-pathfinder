from googlemaps.exceptions import TransportError, Timeout
from settings import gmaps
from location import Location
from car import Car


class Travel:

    def __init__(self, origin, destination, car):
        # Status goes to True if the path is valid.
        self.status = False
        self.origin = Location(origin)
        self.destination = Location(destination)
        self.car = car

        self.distance = 0
        self.duration = 0
        self.steps = []
        self.waypoints = False

        if self.is_travel_possible():
            self.retrieve_road_data()

        self.find_empty_battery_location()

    def is_travel_possible(self):
        if self.origin.status and self.destination.status:
            return True
        else:
            return False

    def retrieve_road_data(self):
        try:
            direction = gmaps.directions('place_id:' + self.origin.key, 'place_id:' + self.destination.key)
        except (TransportError, Timeout):
            pass
        else:
            self.status = True
            self.distance = direction[0]['legs'][0]['distance']['value']
            self.duration = direction[0]['legs'][0]['duration']['value']

            for step in direction[0]['legs'][0]['steps']:
                step_data = {'distance': step['distance']['value'],
                             'duration': step['duration']['value'],
                             'start_location': {'lat': step['start_location']['lat'],
                                                'lng': step['start_location']['lng']}
                             }
                self.steps.append(step_data)

    def find_empty_battery_location(self):
        distance_max = self.car.math_distance_max(15)

        if distance_max >= self.distance:
            self.waypoints = []
            distance = 0

            for step in self.steps:
                if distance_max < distance + step['duration']:
                    self.waypoints.append(step['start_location'])
                    distance = 0
                else:
                    distance += step['duration']

car = Car('bmw', 100, 25)
way = Travel("SNCB Mons Station", "Chaussee de Beaumont 401/A, 7022 Mons, Belgique", car)
print way.steps
