from settings import gmaps


def get_direct_road_step(origin, destination):
    directions_result = gmaps.directions('place_id:' + origin, 'place_id:' + destination)


