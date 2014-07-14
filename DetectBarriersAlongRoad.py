# ---------------------------------------------------------------------------
# Detect Barriers Along Road
# Last Update: 07/01/2014
# Author: Satoshi Miyazawa
# koitaroh@gmail.com
# Detect barriers for mode change at intersections between illicit grid and road
# Parameters: rasterWorkspace(workspace), intersectionPoint(feature layer), dissolvedStreet(feature layer), signitureFile(file), illicitGrid_rook(feature layer), resultWorkspace(workspace)
# Require: arcpy(ArcGIS)
# Developed for ArcGIS 10.2.2

# Update Note: added get count function
# ---------------------------------------------------------------------------

import os, sys, traceback, arcpy
arcpy.env.overwriteOutput = 1 # enable overwriting
arcpy.CheckOutExtension("Spatial")

try:
    # load the point featrure class 
    defaultWorkspace = "C://Users/koitaroh/Documents/ArcGIS/Default.gdb"
    rasterWorkspace = arcpy.GetParameterAsText(0)
    arcpy.env.workspace = rasterWorkspace
    intersectionPoint = arcpy.GetParameterAsText(1)
    dissolvedStreet = arcpy.GetParameterAsText(2)
    signitureFile = arcpy.GetParameterAsText(3)
    illicitGrid_rook = arcpy.GetParameterAsText(4)
    resultWorkspace = arcpy.GetParameterAsText(5)
    polygonBoundary = "C://Users/koitaroh/Documents/ArcGIS/Default.gdb/polygonBoundary"
    buffferAtIntersections = "C://Users/koitaroh/Documents/ArcGIS/Default.gdb/bufferAtIntersections"
    clipStreet = "C://Users/koitaroh/Documents/ArcGIS/Default.gdb/clipStreet"
    buffferAtIntersections_2 = "C://Users/koitaroh/Documents/ArcGIS/Default.gdb/bufferAtIntersections_2"
    featureToPolygonResult = "C://Users/koitaroh/Documents/ArcGIS/Default.gdb/featureToPolygonResult"
    barrierBuffer_layer = "F://HumanTrafficking/barrierBuffer_layer"
    
    iterateRaster = arcpy.ListRasters()
    for raster in iterateRaster:
        arcpy.AddMessage(raster)
        constRaster = arcpy.sa.CreateConstantRaster(1, "INTEGER", raster, raster)
        arcpy.RasterToPolygon_conversion(constRaster, polygonBoundary, "SIMPLIFY", "VALUE")
        arcpy.SelectLayerByLocation_management(intersectionPoint, "INTERSECT", polygonBoundary)
        # arcpy.SelectLayerByLocation_management(dissolvedStreet, "INTERSECT", polygonBoundary)
        result = arcpy.GetCount_management(intersectionPoint)
        count = int(result.getOutput(0))
        if count:
            # arcpy.AddMessage(count)
            arcpy.AddMessage("Number of intersections: {0}".format(count))
            arcpy.Buffer_analysis(intersectionPoint, buffferAtIntersections, "50 Meters", "", "", "ALL")
            arcpy.Clip_analysis(dissolvedStreet, polygonBoundary, clipStreet)
            arcpy.MultipartToSinglepart_management(buffferAtIntersections, buffferAtIntersections_2)
            arcpy.FeatureToPolygon_management([buffferAtIntersections_2, clipStreet], featureToPolygonResult, "", "NO_ATTRIBUTES")
            barrierBuffer = resultWorkspace + "/barrierBuffer_" + raster
            barrierPoint_Walk = resultWorkspace + "/barrierPoint_Walk_" + raster
            barrierPoint_Drive = resultWorkspace + "/barrierPoint_Drive_" + raster
            arcpy.Identity_analysis(buffferAtIntersections_2, featureToPolygonResult, barrierBuffer, "", "1 Meters")
            result = arcpy.GetCount_management(barrierBuffer)
            count2 = int(result.getOutput(0))
            if count2:
                mlcOut = arcpy.sa.MLClassify(raster, signitureFile)
                mlcOut.save(resultWorkspace + "/MLC_" + raster)
                mlcRaster = resultWorkspace + "/MLC_" + raster
                resultTable = resultWorkspace + "/barrierTable_" + raster
                arcpy.sa.TabulateArea(barrierBuffer, "OBJECTID", mlcRaster, "VALUE", resultTable)
                arcpy.AddField_management(resultTable, "RatioDeveloped", "DOUBLE")
                arcpy.AddField_management(resultTable, "RatioForest", "DOUBLE")
                arcpy.AddField_management(resultTable, "RatioShrub", "DOUBLE")
                arcpy.AddField_management(resultTable, "RatioWater", "DOUBLE")
                arcpy.AddField_management(resultTable, "RatioBarren", "DOUBLE")
                arcpy.AddField_management(resultTable, "RatioGrass", "DOUBLE")
                arcpy.AddField_management(resultTable, "RatioPavement", "DOUBLE")
                arcpy.AddField_management(resultTable, "BarrierDrive", "SHORT")
                arcpy.AddField_management(resultTable, "BarrierWalk", "SHORT")
                arcpy.CalculateField_management(resultTable, "RatioDeveloped", "[VALUE_1] / ([VALUE_1] + [VALUE_2] + [VALUE_3] + [VALUE_5] + [VALUE_6] + [VALUE_7])", "VB", "")
                arcpy.CalculateField_management(resultTable, "RatioForest", "[VALUE_2] / ([VALUE_1] + [VALUE_2] + [VALUE_3] + [VALUE_5] + [VALUE_6] + [VALUE_7])", "VB", "")
                arcpy.CalculateField_management(resultTable, "RatioShrub", "[VALUE_3] / ([VALUE_1] + [VALUE_2] + [VALUE_3] + [VALUE_5] + [VALUE_6] + [VALUE_7])", "VB", "")
                arcpy.CalculateField_management(resultTable, "RatioWater", "0", "VB", "")
                arcpy.CalculateField_management(resultTable, "RatioBarren", "[VALUE_5] / ([VALUE_1] + [VALUE_2] + [VALUE_3] + [VALUE_5] + [VALUE_6] + [VALUE_7])", "VB", "")
                arcpy.CalculateField_management(resultTable, "RatioGrass", "[VALUE_6] / ([VALUE_1] + [VALUE_2] + [VALUE_3] + [VALUE_5] + [VALUE_6] + [VALUE_7])", "VB", "")
                arcpy.CalculateField_management(resultTable, "RatioPavement", "[VALUE_7] / ([VALUE_1] + [VALUE_2] + [VALUE_3] + [VALUE_5] + [VALUE_6] + [VALUE_7])", "VB", "")
                lstFields = arcpy.ListFields(resultTable)
                for field in lstFields:
                    # arcpy.AddMessage(field.name)
                    if field.name == "VALUE_4":
                        arcpy.CalculateField_management(resultTable, "RatioDeveloped", "[VALUE_1] / ([VALUE_1] + [VALUE_2] + [VALUE_3] + [VALUE_4] + [VALUE_5] + [VALUE_6] + [VALUE_7])", "VB", "")
                        arcpy.CalculateField_management(resultTable, "RatioForest", "[VALUE_2] / ([VALUE_1] + [VALUE_2] + [VALUE_3] + [VALUE_4] + [VALUE_5] + [VALUE_6] + [VALUE_7])", "VB", "")
                        arcpy.CalculateField_management(resultTable, "RatioShrub", "[VALUE_3] / ([VALUE_1] + [VALUE_2] + [VALUE_3] + [VALUE_4] + [VALUE_5] + [VALUE_6] + [VALUE_7])", "VB", "")
                        arcpy.CalculateField_management(resultTable, "RatioWater", "[VALUE_4] / ([VALUE_1] + [VALUE_2] + [VALUE_3] + [VALUE_4] + [VALUE_5] + [VALUE_6] + [VALUE_7])", "VB", "")
                        arcpy.CalculateField_management(resultTable, "RatioBarren", "[VALUE_5] / ([VALUE_1] + [VALUE_2] + [VALUE_3] + [VALUE_4] + [VALUE_5] + [VALUE_6] + [VALUE_7])", "VB", "")
                        arcpy.CalculateField_management(resultTable, "RatioGrass", "[VALUE_6] / ([VALUE_1] + [VALUE_2] + [VALUE_3] + [VALUE_4] + [VALUE_5] + [VALUE_6] + [VALUE_7])", "VB", "")
                        arcpy.CalculateField_management(resultTable, "RatioPavement", "[VALUE_7] / ([VALUE_1] + [VALUE_2] + [VALUE_3] + [VALUE_4] + [VALUE_5] + [VALUE_6] + [VALUE_7])", "VB", "")
                cursor = arcpy.da.UpdateCursor(resultTable, ["RatioDeveloped", "RatioForest", "RatioShrub", "RatioWater", "RatioBarren", "RatioGrass", "RatioPavement", "BarrierDrive", "BarrierWalk"])
                for row in cursor:
                    row[7] = 0
                    row[8] = 0
                    if row[3] >= 0.1:
                        row[7] = 1
                        row[8] = 1
                    if row[0] + row[1] >= 0.5:
                        row[8] = 1
                    if row[0] + row[1] + row[2] + row[5] >= 0.5:
                        row[7] = 1
                    cursor.updateRow(row)
                del cursor
                arcpy.JoinField_management(barrierBuffer, "OBJECTID", resultTable, "OBJECTID_1", ["RatioDeveloped", "RatioForest", "RatioShrub", "RatioWater", "RatioBarren", "RatioGrass", "RatioPavement", "BarrierDrive", "BarrierWalk"])

        # Barrier Points for Driving
                if(barrierBuffer):
                    barrierBuffer_layer = arcpy.MakeFeatureLayer_management(barrierBuffer, "barrierBuffer_layer", "BarrierDrive = 1")
                    arcpy.Intersect_analysis([barrierBuffer_layer, illicitGrid_rook], "barrierPoint_Drive", "ONLY_FID", "","POINT")
                    barrierPoint_Drive_layer = arcpy.MakeFeatureLayer_management("barrierPoint_Drive", "barrierPoint_Drive_layer")
                    arcpy.SelectLayerByLocation_management(barrierPoint_Drive_layer, "INTERSECT", dissolvedStreet)
                    arcpy.SelectLayerByAttribute_management(barrierPoint_Drive_layer, "SWITCH_SELECTION")
                    arcpy.CopyFeatures_management(barrierPoint_Drive_layer, barrierPoint_Drive)
                    if arcpy.Exists(barrierBuffer_layer): arcpy.Delete_management(barrierBuffer_layer)
                    if arcpy.Exists(barrierPoint_Drive_layer): arcpy.Delete_management(barrierPoint_Drive_layer)

                    # Barrier Points for Driving
                    barrierBuffer_layer = arcpy.MakeFeatureLayer_management(barrierBuffer, "barrierBuffer_layer", "BarrierWalk = 1")
                    arcpy.Intersect_analysis([barrierBuffer_layer, illicitGrid_rook], "barrierPoint_Walk", "ONLY_FID", "","POINT")
                    barrierPoint_Walk_layer = arcpy.MakeFeatureLayer_management("barrierPoint_Walk", "barrierPoint_Walk_layer")
                    arcpy.SelectLayerByLocation_management(barrierPoint_Walk_layer, "INTERSECT", dissolvedStreet)
                    arcpy.SelectLayerByAttribute_management(barrierPoint_Walk_layer, "SWITCH_SELECTION")
                    arcpy.CopyFeatures_management(barrierPoint_Walk_layer, barrierPoint_Walk)
                    if arcpy.Exists(barrierBuffer_layer): arcpy.Delete_management(barrierBuffer_layer)
                    if arcpy.Exists(barrierPoint_Walk_layer): arcpy.Delete_management(barrierPoint_Walk_layer)

except arcpy.ExecuteError:
    arcpy.AddError(arcpy.GetMessages(2))

except:
    tb = sys.exc_info()[2]
    tbinfo = traceback.format_tb(tb)[0]
    arcpy.AddError("Non-tool error occurred")
    # Concatenate information together concerning the error into a message string
    #
    pymsg = "PYTHON ERRORS:\nTraceback info:\n" + tbinfo + "\nError Info:\n" + str(sys.exc_info()[1])
    msgs = "ArcPy ERRORS:\n" + arcpy.GetMessages(2) + "\n"

    # Return python error messages for use in script tool or Python Window
    #
    arcpy.AddError(pymsg)
    arcpy.AddError(msgs)