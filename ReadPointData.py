import arcpy
import numpy as np

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


coords = SHPtoLatLong("C:\Users\DTORERO\Documents\Python\SHP base\Network Analysis.gdb\Nodes")

for array in coords:
    print("Lat:", array[0], "   Long:", array[1])