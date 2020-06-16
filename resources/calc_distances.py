import numpy as np

lat_long_london = (51.506, -0.1272)


def calc_haversine_dist_miles(lat_1, long_1, lat_long_2=lat_long_london, earth_radius=3956):
    """
    Vectorised Haversine formula.
    Reference to https://www.movable-type.co.uk/scripts/latlong.html and https://en.wikipedia.org/wiki/Haversine_formula
    Receives vector with the latitude and longitude of the user and a tuple with the latitude and longitude of the reference point, e.g., London
    By default, distance returned in miles, to get km change earth radius to earth_radius=6371

    """
    
    # Convert city coordinates into a vector to perform vectorised calculation
    assert len(lat_1) == len(long_1)
    vector_ones = np.ones(len(lat_1))
    lat_2 = vector_ones * lat_long_2[0]
    long_2 = vector_ones * lat_long_2[1]

    # Convert degrees to radians
    latitude_1, longitude_1, latitude_2, longitude_2 = np.radians(
        [lat_1, long_1, lat_2, long_2])

    delta_long = longitude_1 - longitude_2
    delta_lat = latitude_1 - latitude_2

    a = (np.sin(delta_lat/2))**2 + np.cos(latitude_1) * \
        np.cos(latitude_2) * (np.sin(delta_long/2))**2
    c = 2 * np.arcsin(np.sqrt(a))
    distance = earth_radius * c

    return distance


def calc_equirectangular_dist_miles(lat_1, long_1, lat_long_2=lat_long_london, earth_radius=3956):
    """
    Faster, but less accurate than the Haversine formula, poor over long distances. 
    By default, distance returned in miles, to get km change earth radius to earth_radius=6371

    """

    assert len(lat_1) == len(long_1)

    # Convert city coordinates into a vector to perform vectorised calculation
    assert len(lat_1) == len(long_1)
    vector_ones = np.ones(len(lat_1))
    lat_2 = vector_ones * lat_long_2[0]
    long_2 = vector_ones * lat_long_2[1]

    # Convert degrees to radians
    latitude_1, longitude_1, latitude_2, longitude_2 = np.radians(
        [lat_1, long_1, lat_2, long_2])

    x = (longitude_2 - longitude_1) * np.cos(0.5 * (latitude_1 + latitude_2))
    y = latitude_2 - latitude_1

    distance = earth_radius * np.sqrt(x*x + y*y)


    return distance
