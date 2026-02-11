import math

def lonlat_distance(a, b):
    a_lon, a_lat = a
    b_lon, b_lat = b
    degree_to_meters_factor = 111 * 1000
    radians_lat = math.radians((a_lat + b_lat) / 2.)
    cos_lat = math.cos(radians_lat)
    dx = abs(a_lon - b_lon) * degree_to_meters_factor * cos_lat
    dy = abs(a_lat - b_lat) * degree_to_meters_factor
    distance = math.sqrt(dx * dx + dy * dy)
    return distance