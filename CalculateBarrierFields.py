# -*- coding: utf-8 -*-
# ---------------------------------------------------------------------------
# CaclusateBarrierFields.py
# Created on: 2014-04-14 1046
# Description: 
# ---------------------------------------------------------------------------

# Import arcpy module
import arcpy

try:
    TabulateTable = arcpy.GetParameterAsText(0)
    output = arcpy.GetParameterAsText(1)
    # Check if fields exist
    lstFields = arcpy.ListFields(TabulateTable)
    arcpy.CalculateField_management(TabulateTable, "sum", "[VALUE_1] + [VALUE_2] + [VALUE_3] + [VALUE_5] + [VALUE_6] + [VALUE_7]", "VB", "")
    arcpy.CalculateField_management(TabulateTable, "RatioDeveloped", "[VALUE_1] / [sum]", "VB", "")
    arcpy.CalculateField_management(TabulateTable, "RatioForest", "[VALUE_2] / [sum]", "VB", "")
    arcpy.CalculateField_management(TabulateTable, "RatioShrub", "[VALUE_3] / [sum]", "VB", "")
    arcpy.CalculateField_management(TabulateTable, "RatioWater", 0, "VB", "")
    arcpy.CalculateField_management(TabulateTable, "RatioGrass", "[VALUE_6] / [sum]", "VB", "")
    
    for field in lstFields:
        arcpy.AddMessage(field.name)
        if field.name == "VALUE_4":
            # Process: Calculate Field (2)
            arcpy.CalculateField_management(TabulateTable, "sum", "[sum] + [VALUE_4]", "VB", "")
            arcpy.CalculateField_management(TabulateTable, "RatioWater", "[VALUE_4] / [sum]", "VB", "")
        
except:
    print arcpy.GetMessages(2)   
