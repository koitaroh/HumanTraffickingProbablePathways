#CreatePairForLine_1km
#Create pairs for 100m grid

import sys, arcpy
arcpy.env.overwriteOutput = 1 # enable overwriting

try:
    # load the point featrure class
    # arcpy.env.workspace = arcpy.GetParameterAsText(0)
    # fc = "C:/Users/koitaroh/Docments/ArcGIS/Default.gdb/WeightPoint_Test"
    fc = arcpy.GetParameterAsText(0)
    outtable_path = arcpy.GetParameterAsText(1)
    # fc = "F:/HumanTrafficking/HumanTrafficking_UTM_Sub.gdb/Fishnet_point_140114_1049"
    # outtable_path = 

    # define variables
    fields = ["POINT_X", "POINT_Y", "pointid"]
    xcoord = 0.0
    ycoord = 0.0
    pointid = 0
    # print("INITIALIZED")

    # create a insert cursor
    cursor2 = arcpy.da.InsertCursor(outtable_path, ("pointid", "origin_x", "origin_y", "destination_x", "destination_y"))
    # create a search cursor
    # insert pairs to table
    with arcpy.da.SearchCursor(fc, fields) as cursor1:
        for row in cursor1:
            xcoord = row[0]
            ycoord = row[1]
            pointid = row[2]
            cursor2.insertRow((rowid, xcoord+100, ycoord, xcoord, ycoord, height, landcover, slope))
            cursor2.insertRow((rowid, xcoord, ycoord+100, xcoord, ycoord, height, landcover, slope))
            cursor2.insertRow((rowid, xcoord-100, ycoord, xcoord, ycoord, height, landcover, slope))
            cursor2.insertRow((rowid, xcoord, ycoord-100, xcoord, ycoord, height, landcover, slope))
            cursor2.insertRow((rowid, xcoord+100, ycoord+100, xcoord, ycoord, height, landcover, slope))
            cursor2.insertRow((rowid, xcoord+100, ycoord-100, xcoord, ycoord, height, landcover, slope))
            cursor2.insertRow((rowid, xcoord-100, ycoord+100, xcoord, ycoord, height, landcover, slope))
            cursor2.insertRow((rowid, xcoord-100, ycoord-100, xcoord, ycoord, height, landcover, slope))

            #rows = arcpy.da.SearchCursor(fc, "POINT_X" between x+10 and x-10 AND "POINT_Y" between y+10 and y-10 )
        del cursor1
        del cursor2

except:
    print arcpy.GetMessages(2)   
