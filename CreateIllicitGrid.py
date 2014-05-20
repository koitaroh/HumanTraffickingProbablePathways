# Create Illicit Grid
# Last Update: 05/17/2014
# Author: Satoshi Miyazawa
# koitaroh@gmail.com
# Create grid polyline feature class from point feature class
# Parameters: workspace, inPoint, pointInterval, outLine
# Require: arcpy(ArcGIS)
# Developed for ArcGIS 10.2.1

# Update Note: remove outTable from parameters

import sys, arcpy
arcpy.env.overwriteOutput = 1 # enable overwriting

try:
    # load the point featrure class 
    arcpy.env.workspace = arcpy.GetParameterAsText(0)
    workspace = arcpy.env.workspace
    inPoint = arcpy.GetParameterAsText(1)
    pointInterval = arcpy.GetParameterAsText(2)
    outTable = "outTable"
    outLine = arcpy.GetParameterAsText(3)

    # define variables
    fields = ["POINT_X", "POINT_Y", "pointid"]
    xcoord = 0.0
    ycoord = 0.0
    pointid = 0
    lineid = 0

    # Create table
    arcpy.CreateTable_management("", outTable)
    arcpy.AddField_management(outTable, "pointid", "LONG")
    arcpy.AddField_management(outTable, "lineid", "LONG")
    arcpy.AddField_management(outTable, "origin_x", "DOUBLE")
    arcpy.AddField_management(outTable, "origin_y", "DOUBLE")
    arcpy.AddField_management(outTable, "destination_x", "DOUBLE")
    arcpy.AddField_management(outTable, "destination_y", "DOUBLE")

    # create a insert cursor
    cursor2 = arcpy.da.InsertCursor(outTable, ("pointid", "lineid", "origin_x", "origin_y", "destination_x", "destination_y"))
    with arcpy.da.SearchCursor(inPoint, fields) as cursor1:
        for row in cursor1:
            xcoord = row[0]
            ycoord = row[1]
            pointid = row[2]
            cursor2.insertRow((pointid, lineid, xcoord+pointInterval, ycoord, xcoord, ycoord))
            lineid += 1
            cursor2.insertRow((pointid, lineid, xcoord, ycoord+pointInterval, xcoord, ycoord))
            lineid += 1
            cursor2.insertRow((pointid, lineid, xcoord-pointInterval, ycoord, xcoord, ycoord))
            lineid += 1
            cursor2.insertRow((pointid, lineid, xcoord, ycoord-pointInterval, xcoord, ycoord))
            lineid += 1
            cursor2.insertRow((pointid, lineid, xcoord+pointInterval, ycoord+pointInterval, xcoord, ycoord))
            lineid += 1
            cursor2.insertRow((pointid, lineid, xcoord+pointInterval, ycoord-pointInterval, xcoord, ycoord))
            lineid += 1
            cursor2.insertRow((pointid, lineid, xcoord-pointInterval, ycoord+pointInterval, xcoord, ycoord))
            lineid += 1
            cursor2.insertRow((pointid, lineid, xcoord-pointInterval, ycoord-pointInterval, xcoord, ycoord))
            lineid += 1

            #rows = arcpy.da.SearchCursor(inPoint, "POINT_X" between x+10 and x-10 AND "POINT_Y" between y+10 and y-10 )
        del cursor1
        del cursor2

    arcpy.XYToLine_management(outTable, outLine, "origin_x", "origin_y", "destination_x", "destination_y","", "pointid", inPoint)

except:
    print arcpy.GetMessages(2)   
