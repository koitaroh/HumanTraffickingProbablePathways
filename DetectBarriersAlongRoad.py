# Detect Barriers Along Road
# Last Update: 05/20/2014
# Author: Satoshi Miyazawa
# koitaroh@gmail.com
# Detect barriers for mode change at intersections between illicit grid and road
# Parameters: rasterWorkspace(workspace), intersectionPoint(feature layer), dissolvedStreet(feature layer), signitureFile(file), illicitGrid_rook(feature class), resultWorkspace(workspace)
# Require: arcpy(ArcGIS)
# Developed for ArcGIS 10.2.1

# Update Note: added get count function

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
    resultWorkspace = arcpy.GetParameterAsText(5)
    polygonBoundary = "C://Users/koitaroh/Documents/ArcGIS/Default.gdb/polygonBoundary"
    buffferAtIntersections = "C://Users/koitaroh/Documents/ArcGIS/Default.gdb/buffferAtIntersections"
    clipStreet = "C://Users/koitaroh/Documents/ArcGIS/Default.gdb/clipStreet"
    buffferAtIntersections_2 = "C://Users/koitaroh/Documents/ArcGIS/Default.gdb/buffferAtIntersections_2"
    featureToPolygonResult = "C://Users/koitaroh/Documents/ArcGIS/Default.gdb/featureToPolygonResult"

    
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
            arcpy.Buffer_analysis(intersectionPoint, buffferAtIntersections, "50 Meters", "", "", "ALL")
            arcpy.Clip_analysis(dissolvedStreet, polygonBoundary, clipStreet)
            arcpy.MultipartToSinglepart_management(buffferAtIntersections, buffferAtIntersections_2)
            arcpy.FeatureToPolygon_management([buffferAtIntersections_2, clipStreet], featureToPolygonResult, "", "NO_ATTRIBUTES")
            barrierBuffer = resultWorkspace + "/barrierBuffer_" + raster
            arcpy.Identity_analysis(buffferAtIntersections_2, featureToPolygonResult, barrierBuffer)
            result = arcpy.GetCount_management(barrierBuffer)
            count2 = int(result.getOutput(0))
            if count2:
                mlcOut = arcpy.sa.MLClassify(raster, signitureFile)
                mlcOut.save(resultWorkspace + "/MLC_" + raster)
                resultTable = resultWorkspace + "/barrierTable_" + raster
                arcpy.sa.TabulateArea(barrierBuffer, "OID", mlcOut, resultTable)
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
                    arcpy.AddMessage(field.name)
                    if field.name == "VALUE_4":
                        arcpy.CalculateField_management(resultTable, "RatioDeveloped", "[VALUE_1] / ([VALUE_1] + [VALUE_2] + [VALUE_3] + [VALUE_4] + [VALUE_5] + [VALUE_6] + [VALUE_7])", "VB", "")
                        arcpy.CalculateField_management(resultTable, "RatioForest", "[VALUE_2] / ([VALUE_1] + [VALUE_2] + [VALUE_3] + [VALUE_4] + [VALUE_5] + [VALUE_6] + [VALUE_7])", "VB", "")
                        arcpy.CalculateField_management(resultTable, "RatioShrub", "[VALUE_3] / ([VALUE_1] + [VALUE_2] + [VALUE_3] + [VALUE_4] + [VALUE_5] + [VALUE_6] + [VALUE_7])", "VB", "")
                        arcpy.CalculateField_management(resultTable, "RatioWater", "[VALUE_4] / ([VALUE_1] + [VALUE_2] + [VALUE_3] + [VALUE_4] + [VALUE_5] + [VALUE_6] + [VALUE_7])", "VB", "")
                        arcpy.CalculateField_management(resultTable, "RatioBarren", "[VALUE_5] / ([VALUE_1] + [VALUE_2] + [VALUE_3] + [VALUE_4] + [VALUE_5] + [VALUE_6] + [VALUE_7])", "VB", "")
                        arcpy.CalculateField_management(resultTable, "RatioGrass", "[VALUE_6] / ([VALUE_1] + [VALUE_2] + [VALUE_3] + [VALUE_4] + [VALUE_5] + [VALUE_6] + [VALUE_7])", "VB", "")
                        arcpy.CalculateField_management(resultTable, "RatioPavement", "[VALUE_7] / ([VALUE_1] + [VALUE_2] + [VALUE_3] + [VALUE_4] + [VALUE_5] + [VALUE_6] + [VALUE_7])", "VB", "")
                cursor = arcpy.UpdateCursor(resultTable)
                for row in cursor:
                    RatioDeveloped = row.getValue("RatioDeveloped")
                    RatioForest = row.getValue("RatioForest")
                    RatioShrub = row.getValue("RatioShrub")
                    RatioWater = row.getValue("RatioWater")
                    RatioBarren = row.getValue("RatioBarren")
                    RatioGrass = row.getValue("RatioGrass")
                    RatioPavement = row.getValue("RatioPavement")
                    if RatioWater >= 0.1:
                        row.setValue("BarrierDrive", 1)
                        row.setValue("BarrierWalk", 1)
                    if RatioForest + RatioDeveloped >= 0.5:
                        row.setValue("BarrierDrive", 1)
                    if RatioDeveloped + RatioForest + RatioShrub + RatioGrass >= 0.5:
                        row.setValue("BarrierWalk", 1)
                    else:
                        row.setValue("BarrierDrive", 0)
                        row.setValue("BarrierWalk", 0)
            arcpy.AddMessage("Check")
           


except:
    print arcpy.GetMessages(2)   
