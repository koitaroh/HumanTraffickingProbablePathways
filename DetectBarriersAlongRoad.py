# Detect Barriers Along Road
# Last Update: 05/19/2014
# Author: Satoshi Miyazawa
# koitaroh@gmail.com
# Detect barriers for mode change at intersections between illicit grid and road
# Parameters: workspace, rasterWorkspace, intersectionPoint, dissolvedStreet, signitureFile, illicitGrid_rook
# Require: arcpy(ArcGIS)
# Developed for ArcGIS 10.2.1

# Update Note: initial commit

import os, sys, arcpy
arcpy.env.overwriteOutput = 1 # enable overwriting
arcpy.CheckOutExtension("Spatial")

try:
    # load the point featrure class 
    rasterWorkspace = arcpy.GetParameterAsText(0)
    arcpy.env.workspace = rasterWorkspace
    intersectionPoint = arcpy.GetParameterAsText(1)
    dissolvedStreet = arcpy.GetParameterAsText(2)
    signitureFile = arcpy.GetParameterAsText(3)
    illicitGrid_rook = arcpy.GetParameterAsText(4)
    
    iterateRaster = arcpy.ListRasters()
    for raster in iterateRaster:
        constRaster = arcpy.sa.CreateConstantRaster(1, "INTEGER", raster, raster)
        arcpy.RasterToPolygon_conversion(constRaster, "in_memory/polygonBoundary", "SIMPLIFY", "VALUE")
        # Select layer by location
        

    # create a search cursor
        with arcpy.da.SearchCursor(reftable, ("Name")) as cursor:
            for row in cursor:
                if fileinworkspace == row[0]:
                    arcpy.AddMessage(file)
                    # arcpy.AddMessage(row[0])
                    # arcpy.AddMessage(fileinworkspace)
                    # counter = counter + 1
                    arcpy.CopyRaster_management(file, outgeodatabase+"/"+fileinworkspace)
                    # arcpy.CopyRaster_management(file, fileinworkspace)
                    # shutil.copy(file, outgeodatabase)
        del cursor

except:
    print arcpy.GetMessages(2)   
