# -*- coding: utf-8 -*-
# ---------------------------------------------------------------------------
# CreateValidationFields.py
# Created on: 2014-04-14 1251
# Description: 
# ---------------------------------------------------------------------------

# Create Random points within streets_buffer
# Straitification
# Raster to polygon
# Create random points in each strata 
# Convert it to 3m * 3m square (later)
# Record the ground truth and classification result one by one
# Create Confusion matrix

import arcpy
arcpy.env.overwriteOutput = 1 # enable overwriting
arcpy.env.workspace = "c:/Users/koitaroh/Documents/ArcGIS/Default.gdb"

inRaster = arcpy.GetParameterAsText(0)
outPoint = arcpy.GetParameterAsText(1)

try:
    arcpy.RasterToPolygon_conversion(inRaster, "tmpRasterToPolygon", "NO_SIMPLIFY", "Value")

    # Create 10 random points in each class polygon 
    for x in xrange(1,8):
        arcpy.Select_analysis("tmpRasterToPolygon", "tmpRasterToPolygon_%d" % (x), 'gridcode = %d AND Shape_Area >= 9' % (x))
        arcpy.Dissolve_management("tmpRasterToPolygon_%d" % (x), "tmpRasterToPolygon_%d_%d" % (x,x))
        arcpy.CreateRandomPoints_management("c:/Users/koitaroh/Documents/ArcGIS/Default.gdb", "RandomPoints_%d" % (x), "tmpRasterToPolygon_%d_%d" % (x,x), "tmpRasterToPolygon_%d_%d" % (x,x), "10")

except:
    print arcpy.GetMessages(2)
