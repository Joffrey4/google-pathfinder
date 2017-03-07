from googlemaps.exceptions import TransportError, Timeout
from settings import gmaps


class Place:
    """
    Retrieve data of a place from an address with Google Map Geocoding API.

    Address example:
        "Rue Fetis 12, 7000 Mons, Belgique"
        "Rue Fetis 12, Mons, Belgique"
        "Rue Fetis 12, Mons"
        "12 Rue Fetis, Mons"
    """

    def __init__(self, request):
        """
        :param request: The address of a place, formatted as commonly written in Belgium.
        :type request: string
        """
        # Status goes to True if the place is valid
        self.status = False

        # Primary data: latitude, longitude and key (= place_id)
        self.lat = 0
        self.lng = 0
        self.key = ""

        # Check if request is string
        if isinstance(request, str):
            self.set_place_data(request)

    def retrieve_geocode_result(self, address):
        """
        Retrieve data of a place from Google Map API Geocoding.

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

    def set_place_data(self, address):
        """
        Set the data of a place into local variables.

        :param address: the address of a place, formatted as commonly written in Belgium.
        :type address: string
        """
        geocode = self.retrieve_geocode_result(address)
        self.key = geocode[0]['place_id']
        self.lat = geocode[0]['geometry']['location']['lat']
        self.lng = geocode[0]['geometry']['location']['lng']

    def get_key_lat_lng(self):
        """
        Return the latitude, longitude and the key of the place.

        :return: The key, lat and lng values. In a dictionary.
        :rtype: {'key' : string, 'lat': float, 'lng': float}
        """
        return {'key': self.key, 'lat': self.lat, 'lng': self.lng}
