from googlemaps.exceptions import TransportError, Timeout
from settings import gmaps
from src.exceptions import IllegalArgumentError, InvalidLocation


# TODO: mettre les exceptions à la création.
# TODO: Spécifier.

class Location:
    """

    """

    def __init__(self, **kwargs):
        """
        Retrieve the metadata of a location, if this place exist. Metadata can be retrieved from
        an address parameter, a couple of latitude and longitude parameter, or a key (place_id) parameter.

        If multiples locations parameters are entered, they will be selected in this order:
            - key (place_id)
            - lat and lng
            - address

        Address formatting example:
            "Rue Fetis 12, 7000 Mons, Belgique"
            "Rue Fetis 12, Mons, Belgique"
            "Rue Fetis 12, Mons"
            "12 Rue Fetis, Mons"

        :param key: The place_id of a location.
        :type key: string

        :param lat: The latitude of a location. Have to be passed with 'lng' parameter.
        :type lat: float

        :param lng: The longitude of a location. Have to be passed with 'lat' parameter.
        :type lng: float

        :param address: The address of a location, formatted as commonly written in Belgium.
        :type request: string
        """
        # Primary data: key, latitude, longitude and address.
        if kwargs is not None and kwargs != {}:
            self.key = kwargs.get('key')
            self.lat = kwargs.get('lat')
            self.lng = kwargs.get('lng')
            self.address = kwargs.get('address')
        else:
            raise IllegalArgumentError(
                "You need to enter at least one parameter: key(string), lat(float) and lng(float), or address(string)")

        # Secondary data:
        self.near_stations = []

        # Status goes to True if this location is a valid one.
        self.status = False

        # Retrieve metadata of the location.
        self.get_geocode_metadata()

    ##
    #   Functions to retrieve metadata of the location
    ##

    def get_geocode_from_address(self, address):
        """
        Retrieve data of a place from an address.

        :param address: the address of a place, formatted as commonly written in Belgium.
        :type address: string

        :return geocode_result: The data of a place, if the place exists.
        :rtype geocode_result: dictionary
        """
        try:
            geocode_result = gmaps.geocode(address)
        except (TransportError, Timeout):
            pass
        else:
            self.status = True
            return geocode_result

    def get_geocode_from_key_or_latlng(self, key):
        """
        Retrieve data of a place from a key (place_id) of from a tuple of (lat, lng).

        :param key: key (place_id), or tuple of (lat, lng)
        :type key: string, or tuple of float.

        :return geocode_result: The data of a place, if the place exists.
        :rtype geocode_result: dictionary
        """
        try:
            geocode_result = gmaps.reverse_geocode(key)
        except (TransportError, Timeout):
            pass
        else:
            self.status = True
            return geocode_result

    def retrieve_geocode_from_valid_arguments(self):
        """
        Select which method have to be used to retrieve geocode, and call it.

        :return: The data of a place, if the place exists.
        :rtype: dictionary
        """
        if isinstance(self.key, str):
            return self.get_geocode_from_key_or_latlng(self.key)

        elif isinstance(self.lat, float) and isinstance(self.lng, float):
            return self.get_geocode_from_key_or_latlng((self.lat, self.lng))

        elif isinstance(self.address, str):
            return self.get_geocode_from_address(self.address)

        else:
            raise ValueError('You need to enter valid arguments.')

    def get_geocode_metadata(self):
        """
        Set the data of a place into local variables.
        """
        geocode = self.retrieve_geocode_from_valid_arguments()
        if self.status:
            self.key = geocode[0]['place_id']
            self.lat = geocode[0]['geometry']['location']['lat']
            self.lng = geocode[0]['geometry']['location']['lng']
            self.address = geocode[0]['formatted_address']

    ##
    #   Functions to find the nearest charging station
    ##

    def find_all_near_station(self, stations_list, radius):
        """
        :param radius:
        :param stations_list: [ {'id': id, 'lat': lat, 'lng': lng, 'key': key}, ... ]
        :return:
        """
        if self.status:
            for station in stations_list:
                try:
                    distance_between = \
                        gmaps.distance_matrix((self.lat, self.lng), (station['lat'], station['lng']), 'driving',
                                              'fr-FR')['rows'][0]['elements'][0]['distance']['value']
                except (TransportError, Timeout):
                    pass
                else:
                    if distance_between <= radius:
                        self.near_stations.append((distance_between, station['id']))
        else:
            raise InvalidLocation('The entered location is invalid.')

    def get_all_near_station(self, station_list, radius=20000):
        self.find_all_near_station(station_list, radius)
        return self.near_stations

    def get_nearest_station(self, station_list, radius=20000):
        self.find_all_near_station(station_list, radius)

        if self.near_stations:
            nearest_current = self.near_stations[0]

            for station in self.near_stations:
                if station[0] > nearest_current[0]:
                    nearest_current = station
            return nearest_current
        else:
            return False


place = Location()
# place.find_all_near_station([{'id': 0, 'lat': 50.4132557, 'lng': 4.0169406, 'key': "ChIJvRKTuK9FwkcRV6Jc8IqyUt4"}])
