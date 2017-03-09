"""
Defines exceptions that are thrown by the Location, Car and Travel objects.
"""

##
#   Exceptions from Location object
##


class IllegalArgumentError(Exception):
    """
    Exception returned by the a Location object when arguments are invalid.
    """
    def __init__(self, message):
        self.message = message

    def __str__(self):
        if self.message:
            return self.message


class InvalidLocation(Exception):
    """
    Exception returned by the a Location object when Google Map API doesn't find any place.
    """
    def __init__(self, message):
        self.message = message

    def __str__(self):
        if self.message:
            return self.message

##
#   Exceptions from Travel object
##


class ImpossibleTravel(Exception):
    """
    Exception returned by a Travel object when Google Map API doesn't find any valid travel,
    between two valid locations.
    """
    def __init__(self, message):
        self.message = message

    def __str__(self):
        if self.message:
            return self.message


class TooManyWaypoints(Exception):
    """
    Exception returned by a Travel object when there's more than 23 waypoints. Google Map API
    do not allow to find a travel with more than 23 waypoints.
    """
    def __init__(self, message):
        self.message = message

    def __str__(self):
        if self.message:
            return self.message


class NoStationInArea(Exception):
    """
    Exception returned by a Travel object when a location has no charging station in the requested
    radius.
    """
    def __init__(self, message, lat, lng):
        self.message = message
        self.lat = lat
        self.lng = lng

    def __str__(self):
        return self.message + ' Coords: (' + str(self.lat) + ', ' + str(self.lng) + ')'
