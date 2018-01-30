# Script to find the closest point form a Base point in an ArcMap Shapefile
# The project interpreter for this file should be: Python27\ArcGis10.5\python.exe

import numpy as np
import math
import arcpy


def SHPtoLatLong(shapefile, spatialReferenceCode=4326 ):
    """
    :param shapefile: shapefile path with Point Features only
    :param spatialReferenceCode: Name of the Spatial reference. Default is WGS84
    :return: List of numpy arrays with Latitude and Longitude values
    from each point in the shapefile
    List = [numpy.array([Lat,Long])]
    """
    cursor = arcpy.da.SearchCursor(shapefile, ["SHAPE@"])
    projection = arcpy.SpatialReference(spatialReferenceCode)

    coordinates = []

    for row in cursor:
        point = row[0].projectAs(projection)
        longitude = point.firstPoint.X
        latitude = point.firstPoint.Y
        coordinates.append(np.array([latitude, longitude]))

    del cursor

    return coordinates


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


def closestPoint(PointO, PointList):
    """
    Finds the closest point from P0, from a list of points
    :param PointO: Origin Point. array
    :param PointList: List of Points, to find the closest. List of arrays
    :return:
    """
    # Calculate distance from each point in PointList to PointO
    # Insert the data into a dictionary
    distDict = {}
    for point in PointList:
        distance = distanceLatLong(PointO, point)
        distDict[distance] = point

    # Trace the minor distance and return the closest point
    minorDist = min(distDict.keys())
    closest = distDict[minorDist]
    return closest


coords = SHPtoLatLong("Test_Data\Network Analysis.gdb\Nodes")

xyList = coords[1:]
print(xyList)

xyO = coords[0]
print(xyO)

result = closestPoint(xyO, xyList)
print(result)