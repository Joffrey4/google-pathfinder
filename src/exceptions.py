"""
Defines exceptions that are thrown by the Location, Car and Travel objects.
"""


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
    Exception returned by the a Location object when Google Map API doesn't fin any place.
    """
    def __init__(self, message):
        self.message = message

    def __str__(self):
        if self.message:
            return self.message
