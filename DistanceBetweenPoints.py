import arcpy
import math
import numpy as np


def hexToRad(degrees):
    """
    helper function to convert Hexadecimal degrees to Radians
    """
    return degrees*math.pi/180


def distanceLatLong(PointO, PointU):
    """
    Calculates the distance between two points, for Latitude and Longitude
    :param PointO: array([Latitude O,Longitude O])
    :param PointU: array([Latitude U,Longitude U])
    :return: distance between two points
    """
    R = 6371 # Radius of the earth in km
    D = PointU - PointO
    dLat = hexToRad(D[0])
    dLon = hexToRad(D[1])

    # Haversine formula for calculating the distance
    a = math.sin(dLat / 2) ** 2 + math.cos(hexToRad(PointO[0]))*math.cos(hexToRad(PointU[0])) * math.sin(dLon / 2) * math.sin(dLon / 2)
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    distance = R * c

    return distance


PO = np.array([-12.0, -77.0])
PU = np.array([-11.75, -77.25])
d = distanceLatLong(PO, PU)
print(d)
