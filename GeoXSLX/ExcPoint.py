#!/usr/bin/env python
# title           :ExcPoint.py
# description     :Excel point class for geographic analysis.
# author          :AT
# date            :20110930
# version         :0.1
# python_version  :3.6
# ==============================================================================

# Defs


import string
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
                        becomes a dictionary containing field indexes and values
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

def readExcelSheet(filename, sheetname = "Hoja1"):
    """
    Reads an excel file and returns the sheet object
    :param filename: Excel filename
    :param sheetname: Sheet name
    :return: sheet instance
    """
    return openpyxl.load_workbook(filename).get_sheet_by_name(sheetname)


def defineColumnIndexes():
    """Helper function to define Column Indexes in an Excel"""
    columnIndexes = [char for char in string.ascii_uppercase]
    for i in string.ascii_uppercase:
        for j in string.ascii_uppercase:
            columnIndexes.append(i + j)
    return columnIndexes


def readHeader(sheet, header, latNames = ["LAT", "LATITUDE", "Latitud", "Y"],
               longNames = ["LONG", "LONGITUDE", "Longitud", "X"]):
    """
    Reads the header and returns a list of Column names
    :param sheet: sheet to read
    :param header: header row Index
    :param latNames: list of names to consider latitude
    :param longNames: list of names to consider longitude
    :return: a tuple with two components:
            list with [lat, long] indexes
            dictionary with header Index and names:
            {columnIndex (str) -> columnName (str) }
    """

    columnIndexes = defineColumnIndexes()

    latFlag = False
    longFlag = False

    headerDict = {}
    coordList = [0,0]

    index = 0

    cursor = sheet[columnIndexes[index] + str(header)]

    while cursor.value is not None:

        # Check if latitude and longitude are present in the header
        if cursor.value in latNames:
            latFlag = True
            coordList[0] = columnIndexes[index]
        if cursor.value in longNames:
            longFlag = True
            coordList[1] = columnIndexes[index]

        # Reading data from header
        headerDict[columnIndexes[index]] = cursor.value
        index += 1
        cursor = sheet[columnIndexes[index] + str(header)]

    # Return if latitude and longitude are present in the header
    if latFlag and longFlag:
        return (coordList, headerDict)
    else:
        raise ValueError("Latitude and Longitude not present in the header")


def readRow(rowIndex, sheet, columnList):
    """
    helper function to read each row of the sheet and retrieve data
    :param rowIndex: index of row to read
    :param sheet: sheet to read
    :param columnList: list of column Indexes
    :return: a dictionary: columnIndex -> data
    """

    rowData = {}

    for index in columnList:
        cursor = sheet[index + str(rowIndex)]
        rowData[index] = cursor.value

    return rowData


def searchCol(columnNameList, sheet, header = 1):
    """
    Helper function
    :param columnNameList: list of strings, possible names of the column to search
    :param sheet: sheet to look into
    :param header: the index of the header row
    :return: Index of column to search, as a letter
    """

    columnIndexes = defineColumnIndexes()

    index = 0
    cursor = sheet[columnIndexes[index] + str(header)]
    while cursor.value is not None:
        if cursor.value in columnNameList:
            return columnIndexes[index]
        index += 1
        cursor = sheet[columnIndexes[index] + str(header)]
    raise ValueError("Column " + columnNameList + " not in Worksheet")


def sortByFunction(itemList, orderFunction, limit = math.pi):
    """
    orders the itmes by a determined property of the items
    :param itemListWork: list of items to be ordered
    :param orderFunction: function to apply to the items. the result determines the order in wich the items will be
                          sorted. It must return a type in wich < > operations can be applied.
    :param limit: the max value of the orderFunction(itemList) to be considered.
                  after reached that value, the sorting algorith stops
    :return: Tuple with:    (list of items sorted, by orderFunction result, until the limit stablished and
                            ordered variable - index of sorted number until limit)
    """

    itemListWork = itemList.copy()

    funcList = [orderFunction(item) for item in itemListWork]

    # Pi is just a non probable value to define the limit
    # So, If the user doesn't sets a value, its considered the maximum possible value in the funcList
    if limit == math.pi:
        limit = max(funcList)

    ordered = 0
    n = len(itemListWork)

    # Enter the loop until all values are sorted or the limit is reached
    while ordered <= n - 1 and funcList[ordered] < limit:

        index = -1
        while index >= ordered - n + 1:
            # Compare values of index and preindex in funcList
            if funcList[index] < funcList[index - 1]:
                # Flip index with preindex in both lists
                (itemListWork[index], itemListWork[index - 1]) = (itemListWork[index - 1], itemListWork[index])
                (funcList[index], funcList[index - 1]) = (funcList[index - 1], funcList[index])
            index -= 1

        ordered += 1

    return (itemListWork, ordered)


def pointMap(filename, sheetname = "Hoja1", header = 1):
    """
    Transforms a xlsx file into a list of ExcPoints
    :param filename: filename of the Excel workbook
    :param sheet: name of the sheet in wich the data is
    :param header: index of header row
    :return: list of ExcPoints
    """

    #Read sheet
    sheet = readExcelSheet(filename, sheetname)


    # Read header and find Lat and Long Columns

    headerData = readHeader(sheet, header)
    fields = headerData[1]
    latIndex = headerData[0][0]
    longIndex = headerData[0][1]

    # create point for each row and append to list

    pointList = []

    i = header + 1
    cursor = sheet["A"+str(i)]
    while cursor.value is not None:
        latValue = sheet[latIndex+str(i)].value
        longValue = sheet[longIndex+str(i)].value
        coordinates = np.array([latValue, longValue])

        data = readRow(i,sheet, fields.keys())

        newPoint = ExcPoint(data,coordinates)
        pointList.append(newPoint)

        i += 1
        cursor = sheet["A" + str(i)]

    return pointList


# ==============================================================================

# Main

# Read file and transform to PointMap
filename = "C:/Users/DTORERO/Documents/Python/Geographic_Analysis/Geographic_Analysis/GeoXSLX/sheet_test.xlsx"
sheetname = "Hoja1"
header = 1

filenameToSave = "C:/Users/DTORERO/Documents/Python/Geographic_Analysis/Geographic_Analysis/GeoXSLX/sheet_test_results.xlsx"

pointList = pointMap(filename, sheetname, header)

book = openpyxl.load_workbook(filename)

sheet = book.get_sheet_by_name(sheetname)


# search particular columns (MPF)

nameMPF = ["CANTIDAD DE MPF", "MPF", "MODULOS PREFABRICADOS"]
columnIndexMPF = searchCol(nameMPF, sheet)
print("Column index for MPF: " + str(columnIndexMPF))

# Backup original list
pointListBackUp = pointList.copy()

# Enter main loop - One for each group

groupNum = 0

while len(pointList) > 0:

    groupNum += 1
    print("GroupNum: " + str(groupNum))

    # Pick a point based of highest latitude
    lats = [latPoint.get_coords()[0] for latPoint in pointList]
    selectedPoint = pointList[lats.index(max(lats))]

    # Move it to zeroth location
    (pointList[0], pointList[lats.index(max(lats))]) = (selectedPoint, pointList[0])

    # Order Points by proximity from that point
    # Until max distance
    maxDistance = 150
    (pointList, topIndex) = sortByFunction(pointList, pointList[0].distance, maxDistance)

    # Enter inner loop
    # Until all conditions are met
    conditionFlag = True

    # Set initial max amount of IE and MPF
    maxIE = min(12, len(pointList))
    maxMPF = 25

    while conditionFlag:
        # Count max IE
        if topIndex + 1 > maxIE:
            topIndex = maxIE - 1
        else:
            maxIE = topIndex + 1

        # Count max MPF

        print("topIndex: " + str(topIndex))

        countMPF = 0
        for i in range(topIndex + 1):
            currentMPF = pointList[i].get_field_value(columnIndexMPF)
            countMPF += currentMPF

        if countMPF > maxMPF:
            # Tweek scope values for IE
            maxIE -= 1
        else:
            conditionFlag = False

    # Exit inner loop

    #Set group value to points

    for i in range(topIndex + 1):
        pointID = pointList[i].get_id()
        for tryPoint in pointListBackUp:
            if pointID == tryPoint.get_id():
                tryPoint.set_group(groupNum)

    #Split list

    print("PointListLenght: " + str(len(pointList)))
    print("Number of items in group: " + str(topIndex+1))

    pointList = pointList[topIndex + 1:]

    print("PointListLenght after cut: " + str(len(pointList)))

# Write Excel file with group values

columnIndexes = defineColumnIndexes()
columnToWrite = columnIndexes[len(pointListBackUp[0].get_fields())]

sheet[columnToWrite + str(header)].value = "Grupos de Inspección"

for point in pointListBackUp:
    sheet[columnToWrite + str(point.get_id() + header)].value = point.get_group()

# Save Excel File
book.save(filenameToSave)
print("Edited file saved as " + filenameToSave)

# ==============================================================================