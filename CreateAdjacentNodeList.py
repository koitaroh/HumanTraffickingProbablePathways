# ---------------------------------------------------------------------------
# CreateAdjacentNodeList.py
# Date:    11/06/2010
# Last update: 07/11/2014 10:48
# Author:  Liz Groff & Jo Fraley
# Modified by Satoshi Miyazawa
# Developed for ArcGIS 10.3 (ArcGIS Pro)
# Purpose: Find the nodes that are accessible from each node in the feature layer
# ---------------------------------------------------------------------------

# Import system modules
import arcpy
import os

# Get the tool parameter values
nodefc = arcpy.GetParameterAsText(0)
streetfc = arcpy.GetParameterAsText(1)
uniquefield = arcpy.GetParameterAsText(2)
thefile = arcpy.GetParameterAsText(3)

#Create a new file to write out nearbyNodes to
try:
    report = open(thefile, 'w')
except:
    print (arcpy.GetMessages())

try:
    columnNames = "Active,Node1,Node2,Node3,Node4,Node5,Node6"
    report.write(columnNames+"\n")
except:
    print (arcpy.GetMessages())
    
#Layer Variables - convert the shape files to layer files
#Make the layer file for nodes
try:
    arcpy.management.MakeFeatureLayer(nodefc, 'nodeLYR')

except:
    #If an error occured print the message to the screen
    print (arcpy.GetMessages())

#Make the layer file for streets
try:
    arcpy.management.MakeFeatureLayer(streetfc, 'streetLYR')

except:
    #If an error occured print the message to the screen
    print (arcpy.GetMessages())

#Select all the nodes in the strnodes2 layer
try:
    rows = arcpy.SearchCursor(nodefc)
except:
    arcpy.GetMessages()

#Grab the first record in the table
row = rows.next()

#Create a variable to hold the strnode number and set up query
strnode = row.getValue(uniquefield)
query = uniquefield + " = " + str(strnode)

while row != None:
    #select the row as a selection for use in the select by location method
    try:
        arcpy.SelectLayerByAttribute_management("nodeLYR", "NEW_SELECTION", query)
    except:
        #If an error occured print the message to the screen
        arcpy.GetMessages()
        
    #Use selected node to select the intersecting streets
    try: 
        # Process: Select Layer By Location...
        arcpy.SelectLayerByLocation_management("streetLYR", "INTERSECT", "nodeLYR", "10 Feet", "NEW_SELECTION")
    except:
        #If an error occured print the message to the screen
        arcpy.GetMessages()

    #Use selected streets to find the intersecting nodes on opposite end and create a new search cursor
    #that is just for the selected records in nodes
    try: 
        #Process: Select Layer By Location (2)...
        selCursor = arcpy.SearchCursor(arcpy.SelectLayerByLocation_management("nodeLYR", "INTERSECT", "streetLYR", "10 Feet", "NEW_SELECTION"))
    except:
        #If an error occured print the message to the screen
        arcpy.GetMessages()
    
    #Set curRow as the first row of the selected set of records
    currentRow = selCursor.next()

    #Loop through the selected rows adding the adjacent strnodes to the tempNodePlus variable
    tempNodePlus = str(strnode) + ","
    
    i = 0
    while currentRow != None:
        compare = currentRow.getValue(uniquefield)
    
        #If statement to avoid writing the active node to the neighbor file
        if strnode != compare:
            tempList = str(compare) + ","
            tempNodePlus = tempNodePlus + tempList
        i = i + 1
        
        #Retrieve the next record in the selection set    
        currentRow = selCursor.next()
        
    #write out record to file
    report.write(tempNodePlus+"\n")

    #go to next row
    row = rows.next()
    if row != None:
        strnode = row.getValue(uniquefield)
	query = uniquefield + " = " + str(strnode)

#close the file
report.close


             
