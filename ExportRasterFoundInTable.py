# ExportRasterFoundInTable
# Export Raster Files that are found in a table into a geodatabase 

import sys, os, shutil, arcpy
arcpy.env.overwriteOutput = 1 # enable overwriting

try:
    # load the point featrure class
    # arcpy.env.workspace = arcpy.GetParameterAsText(0)
    workspace = arcpy.GetParameterAsText(0)
    reftable = arcpy.GetParameterAsText(1)
    outgeodatabase = arcpy.GetParameterAsText(2)

    # workspace = "F:/HumanTrafficking/NAIP"
    # reftable = "F:/HumanTrafficking/HumanTrafficking_UTM_Sub.gdb/NAIP_Table_Subarea2_140305_1004"

    arcpy.env.workspace = workspace
    # counter = 0
    # for in a workspace
    # for in a table
    # if the file name is found in a table
    # export into a geodatabase
    for file in os.listdir(workspace):
        fileinworkspace = os.path.splitext(os.path.basename(file))[0]
    
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

    # arcpy.AddMessage(counter)


except:
    print arcpy.GetMessages(2)   
