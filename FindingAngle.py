# vertex_angle.py  
# find change in angle along a polyline at each vertex  
# assume :  
# in a projected coordinate system, not dd  
# don't know what to do with output, maybe add value to a point  
# Kim Ollivier  
# 29 October 2010  
#  
import arcpy 
import math  
import sys  
  
arcpy.env.overWriteOutput = True

try:  
    inlay = sys.argv[1]  
except :  
    inlay = "C:\\Users\\jrayer\\Documents\\ArcGIS\\Default.gdb\\____Road"
arcpy.AddField_management(inlay, "angle", "DOUBLE")
desc = arcpy.Describe(inlay)  
shapefield = desc.ShapeFieldName  
cur = arcpy.SearchCursor(inlay)  
row = cur.next()  
n = 0  
m = 0  
p = 0  
while row:  
    feat = row.getValue(shapefield)  
    print "Feature",n  
    for partNum in range(feat.partCount) :  
        part = feat.getPart(partNum)  
        ptLast = None  
        bearingLast = None  
        print "Part",m  
        for ptNum in range(part.count):  
            pt = part.next()   
            if ptLast:  
                bearing = math.atan2((pt.Y - ptLast.Y),(pt.X - ptLast.X))  
                if bearingLast:  
                    delta = bearing - bearingLast
                    angle = delta/math.pi*180.0
                    print p,angle
                    arcpy.CalculateField_management(inlay, "angle", angle)
                bearingLast = bearing  
            ptLast = pt  
            p+=1  
        m+=1  
    n+=1  
    row = cur.next()
del cur,row  
