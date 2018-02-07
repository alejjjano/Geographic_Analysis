#!/usr/bin/env python
# title           :ExcPoint.py
# description     :Excel point class for geographic analysis.
# author          :AT
# date            :20110930
# version         :0.1
# python_version  :3.6
# ==============================================================================

# Defs


import openpyxl
import numpy as np
import math


class ExcPoint(object):
    """
    Container for point information extracted from an Excel file
    """

    idCounter = 0

    def __init__(self, aTable, coords):
        """
        :param id: ObjectID from the class
        :param aTable:  attributes from excel table
                        becomes a dictionary containing fields and values
        :param coords: nympy array containing latitude and longitude
        """
        ExcPoint.idCounter += 1
        self.id = ExcPoint.idCounter

        if isinstance(aTable, dict):
            self.aTable = aTable
        else:
            raise ValueError("Point attributes should be transformed into a dictionary datatype")

        if isinstance(coords, type(np.array([]))):
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

    def set_group(self,group):
        """Sets the value for the group that the point belongs
        :param group: int
        """
        if isinstance(group, int):
            self.group = group
        else:
            raise ValueError("Group value should be an integer")

    def get_group(self):
        return self.group

    def distance(self, other):
        """
        Calculates the distance between two ArcPoint objects,
        from its coordinates values using the Haversine formula
        :param other: ArcPoint Object to calculate distante to
        :return:
        """

        """
        Calculates the distance between two ArcPoint objects,
        from its coordinates values using the Haversine formula
        :param PointO: array([Latitude O,Longitude O])
        :param PointU: array([Latitude U,Longitude U])
        :return: distance between two points
        """

        def hexToRad(degrees):
            """
            helper function to convert Hexadecimal degrees to Radians
            """
            return degrees * math.pi / 180

        PointU = 0

        R = 6371  # Radius of the earth in km
        D = other.get_coords() - self.get_coords()
        dLat = hexToRad(D[0])
        dLon = hexToRad(D[1])

        # Haversine formula for calculating the distance
        a = math.sin(dLat / 2) ** 2 + math.cos(hexToRad(self.get_coords()[0])) * math.cos(hexToRad(other.get_coords()[0])) * math.sin(
            dLon / 2) * math.sin(dLon / 2)
        c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
        distance = R * c

        return distance

# Define variable Column Indexes

def defineColumnIndexes():
    """Helper function to define Column Indexes in an Excel"""
    columnIndexes = [char for char in string.ascii_uppercase]
    for i in string.ascii_uppercase:
        for j in string.ascii_uppercase:
            columnIndexes.append(i + j)
    return columnIndexes


def readHeader(sheet, header, exceptions = []):
    """
    Reads the header and returns a list of Column names
    :param sheet: sheet to read
    :param header: header row Index
    :param exceptions: list of Indexes from columns to ignore
    :return: a dictionary with header Index and names:
            {columnIndex (str) -> columnName (str) }
    """

    columnIndexes = defineColumnIndexes()
    for excepted in exceptions:
        columnIndexes.remove(excepted)

    headerDict = {}

    index = 0
    cursor = sheet[columnIndexes[index] + str(header)]
    while cursor.value is not None:
        headerDict[columnIndexes[index]] = cursor.value
        index += 1
        cursor = sheet[columnIndexes[index] + str(header)]

    return headerDict


def readRow(rowIndex,sheet,columnList):
    """
    helper function to read each row of the sheet and retrieve data
    :param rowIndex: index of row to read
    :param sheet: sheet to read
    :param columnList: list of column Indexes
    :return: a dictionary: columnIndex -> data
    """
    pass


def searchCol(columnNameList, sheet, header):
    """
    Helper function
    :param columnNameList: string, column to search
    :param sheet: sheet to look into
    :param header: the index of the header row
    :return: Index of column to search, as a letter
    """
    pass


def pointMap(filename, sheet = "Hoja 1", header = 1):
    """
    Transforms a xlsx file into a list of ExcPoints
    :param filename: filename of the Excel workbook
    :param sheet: name of the sheet in wich the data is
    :param header: index of header row
    :return: list of ExcPoints
    """

    #Read sheet
    sheet = openpyxl.load_workbook(filename).get_sheet_by_name(sheet)

    # Start of helper function


    #Read header


    columnList =[]





    # End of helper function

    # Find lat and long columns

    latNames = ["LAT", "LATITUDE", "Latidud", "Y"]
    latIndex = searchCol(latNames, sheet, 1)

    longNames = ["LONG", "LONGITUDE", "Longitud", "X"]
    longIndex = searchCol(longNames, sheet, 1)

    l = []

    # create point for each row and append to list

    i = header + 1
    cursor = sheet["A"+str(i)]
    while cursor.value is not None:
        latValue = sheet[latIndex+str(i)]
        longValue = sheet[longIndex+str(i)]
        cx = np.array([latValue, longValue])
        newPoint = ExcPoint({},cx)
        l.append(newPoint)

        i += 1
        cursor = sheet["A" + str(i)]



# ==============================================================================

# Main

# Read file and transform to PointMap
# Backup original list

# Enter main loop - One for each group

    # Pick a point based of lowest latitude

    # Order Points by proximity from that point
    # Or proximity to each other
    # Until max distance

    # Enter inner loop - One for each try

        # Count max IE
        # Count max MPF
        # Count max
        # Tweek scope values for IE

    # Exit inner loop

    #Set goup value to points
    #Split list

# Write Excel file with group values