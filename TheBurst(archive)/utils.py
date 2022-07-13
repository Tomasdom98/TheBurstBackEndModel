from math import radians, cos, sin, asin, sqrt
import re

def haversine(point1, point2):
    """
    Calculate the great circle distance in kilometers between two points
    on the earth (specified in decimal degrees)
    """
    # convert decimal degrees to radians
    lat1, lon1=point1
    lat2, lon2=point2
    lon1, lat1, lon2, lat2 = map(radians, [lon1, lat1, lon2, lat2])

    # haversine formula
    dlon = lon2 - lon1
    dlat = lat2 - lat1
    a = sin(dlat/2)**2 + cos(lat1) * cos(lat2) * sin(dlon/2)**2
    c = 2 * asin(sqrt(a))
    r = 6371 # Radius of earth in kilometers. Use 3956 for miles. Determines return value units.
    return c * r

def coord_converter(coordinates):
    list_=['Nord','Sud','Est','Ouest']
    if any(word in coordinates for word in list_):
        deg, minutes, seconds =  re.split('[°\']', coordinates)
        seconds,direction=seconds.split()
        return (float(deg) + float(minutes)/60 + float(seconds)/(60*60)) * (-1 if direction in ['Sud','Ouest'] else 1)
    else:
        deg, minutes, seconds =  re.split('[°\'"]', coordinates)
        return (float(deg) + float(minutes)/60 + float(seconds)/(60*60))
