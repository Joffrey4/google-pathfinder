from googlemaps.exceptions import TransportError, Timeout
from settings import gmaps


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
            print kwargs
            self.key = kwargs.get('key')
            self.lat = kwargs.get('lat')
            self.lng = kwargs.get('lng')
            self.address = kwargs.get('address')
        else:
            raise ValueError(
                'You need to enter at least one parameter: key(string), lat(float) and lng(float), or address(string)')

        # Status goes to True if this location is a valid one.
        self.status = False

        # Retrieve metadata of the location.
        self.get_geocode_metadata()

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
        print geocode
        if self.status:
            self.key = geocode[0]['place_id']
            self.lat = geocode[0]['geometry']['location']['lat']
            self.lng = geocode[0]['geometry']['location']['lng']
            self.address = geocode[0]['formatted_address']

    # TODO: Fonction pour trouver la borne la plus proche de ce lieu

    def get_key_lat_lng(self):
        """
        Return the latitude, longitude and the key of the place.

        :return: The key, lat and lng values. In a dictionary.
        :rtype: {'key' : string, 'lat': float, 'lng': float}
        """
        return {'key': self.key, 'lat': self.lat, 'lng': self.lng}


place = Location()
print place.key
