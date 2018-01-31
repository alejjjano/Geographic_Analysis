# Script to find the closest point form a Base point in an ArcMap Shapefile
# The project interpreter for this file should be: Python27\ArcGis10.5\python.exe

import numpy as np
import math
import arcpy

class ArcPoint(object):
    """
    Container for point information extracted from an ArcGis shapefile
    """

    def __init__(self, id, aTable, coords):
        """
        :param id: ObjectID in the shapefile
        :param aTable: attribute table from the shapefile
                becomes a dictionary containing fields and values (apart from to ObjectID or shape)
        :param coords: nympy array containing latitude and longitude
        """
        if isinstance(id, int):
            self.id = id
        else:
            raise ValueError("id value should be an int - ObjectID from the shapefile")

        if isinstance(aTable, dict):
            self.aTable = aTable
        else:
            raise ValueError("Attribute table should be transformed into a dictionary datatype")

        if isinstance(coords, numpy.array):
            self.coords = coords
        else:
            raise ValueError("Coordinates should be transformed into a numpy array")

    def get_id(self):
        return self.id

    def get_attributes(self):
        return self.aTable[:]

    def get_fields(self):
        return self.aTable.keys()

    def get_field_value(self, field):
        return self.aTable[field]

    def get_coords(self):
        return self.coords.copy()

    def distance(self, other):
        """
        Calculates the distance between two ArcPoint objects,
        from its coordinates values using the Haversine formula
        :param other: ArcPoint Object to calculate the distance to
        :return:
        """

        """
        Calculates the distance between two ArcPoint objects,
        from its coordinates values using the Haversine formula
        
        
        :param PointO: array([Latitude O,Longitude O])
        :param PointU: array([Latitude U,Longitude U])
        :return: distance between two points
        """
        R = 6371  # Radius of the earth in km
        D = PointU - PointO
        dLat = hexToRad(D[0])
        dLon = hexToRad(D[1])

        # Haversine formula for calculating the distance
        a = math.sin(dLat / 2) ** 2 + math.cos(hexToRad(PointO[0])) * math.cos(hexToRad(PointU[0])) * math.sin(
            dLon / 2) * math.sin(dLon / 2)
        c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
        distance = R * c

        return distance



def SHPtoLatLong(shapefile, spatialReferenceCode = 4326 ):
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