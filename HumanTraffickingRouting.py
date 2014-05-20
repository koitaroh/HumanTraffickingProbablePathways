# HumanTrafficking_Rounting
# Last Update: 05/14/2014
# Author: Satoshi Miyazawa
# koitaroh@gmail.com
# Solve Route analysis using ArcGIS Network Analyst
# Parameters: inNetworkDataset, inFacilities, inIncidents
# Require: arcpy(ArcGIS)
# Developed for ArcGIS 10.2.1

try:
    import arcpy, os, datetime
    arcpy.env.overwriteOutput = 1 # enable overwriting
    arcpy.env.workspace = "C:/Users/koitaroh/Documents/ArcGIS/Default.gdb"
    # Check out ArcGIS Network Analyst license
    arcpy.CheckOutExtension("Network")
    # Set local variables
    inNetworkDataset = arcpy.GetParameterAsText(0)
    # Incidents: Origing, Facilities: Destinations
    inIncidents = arcpy.GetParameterAsText(1)
    inFacilities = arcpy.GetParameterAsText(2)
 
 # Name layers for each scenario
    outNALayerName = "BestRoutes"
    outNALayerName_1 = "Scenario_1"
    outNALayerName_2 = "Scenario_2"
    outNALayerName_3 = "Scenario_3"
    outNALayerName_4 = "Scenario_4"
    outNALayerName_5 = "Scenario_5"
    outNALayerName_6 = "Scenario_6"
    outNALayerName_6 = "Scenario_7"

    impedanceAttribute = "Time"
    accumulateAttributeName = ["Length","Time"]
    
    outRouteFile = "F:/HumanTrafficking/HumanTrafficking_SubArea6.gdb/"
    outLayerFile = "F:/HumanTrafficking/BestRoutes" + "/"

    # define restrictions variables
    arcpy.AddMessage("Creating Closest Facility Layer")
    outNALayer = arcpy.na.MakeClosestFacilityLayer(inNetworkDataset,outNALayerName,
                                                   impedanceAttribute,"TRAVEL_TO",
                                                   "",26, accumulateAttributeName,
                                                   "NO_UTURNS", "")
    arcpy.AddMessage("Closest Facility Layer created")
    arcpy.AddMessage(datetime.datetime.now())
    outNALayer = outNALayer.getOutput(0)
    subLayerNames = arcpy.na.GetNAClassNames(outNALayer)
    facilitiesLayerName = subLayerNames["Facilities"]
    incidentsLayerName = subLayerNames["Incidents"]
    fieldMappings1 = arcpy.na.NAClassFieldMappings(outNALayer, incidentsLayerName)
    fieldMappings1["Name"].mappedFieldName = "Name"
    fieldMappings2 = arcpy.na.NAClassFieldMappings(outNALayer, incidentsLayerName)
    fieldMappings2["Name"].mappedFieldName = "Name"
    
    # Run with Senario 1: Unorganized Smuggling 1
    arcpy.AddMessage("Running Scenario_1.")
    solverProperties = arcpy.na.GetSolverProperties(outNALayer)
    defaultRestrictions = solverProperties.restrictions
    defaultRestrictions += ["Avoid Off-road driving", "Avoid On-road driving"]
    solverProperties.restrictions = defaultRestrictions
    arcpy.na.AddLocations(outNALayer, facilitiesLayerName, inFacilities,
                          fieldMappings1,"","","","","CLEAR","","","EXCLUDE")
    arcpy.na.AddLocations(outNALayer, incidentsLayerName, inIncidents,
                          fieldMappings2,"","","","","CLEAR","","","EXCLUDE")
    arcpy.na.Solve(outNALayer)
    arcpy.AddMessage("Solving.")
    arcpy.AddMessage(datetime.datetime.now())
    for lyr in arcpy.mapping.ListLayers(outNALayer):
        if lyr.name == "Routes":
            arcpy.CopyFeatures_management(lyr, outRouteFile + "Scenario_1")
    arcpy.AddField_management(outRouteFile + "Scenario_1", "scenarioid", "SHORT")
    arcpy.CalculateField_management(outRouteFile + "Scenario_1", "scenarioid", 1)
    arcpy.AddMessage("Layer for Scenario_1 saved.")
    arcpy.AddMessage(datetime.datetime.now())
    
    # Run with Scenario 2: Unorganized Smuggling 2
    arcpy.AddMessage("Running Scenario_2.")
    solverProperties = arcpy.na.GetSolverProperties(outNALayer)
    defaultRestrictions = solverProperties.restrictions
    defaultRestrictions += ["Avoid City", "Avoid Open Area", "Prefer Ephemeral River", "Prefer Federal Land", "Prefer Indian Reservation", "Prefer Northern Visibility"]
    solverProperties.restrictions = defaultRestrictions
    arcpy.na.AddLocations(outNALayer, facilitiesLayerName, inFacilities,
                          fieldMappings1,"","","","","CLEAR","","","EXCLUDE")
    arcpy.na.AddLocations(outNALayer, incidentsLayerName, inIncidents,
                          fieldMappings2,"","","","","CLEAR","","","EXCLUDE")
    arcpy.AddMessage("Solving.")
    arcpy.AddMessage(datetime.datetime.now())
    arcpy.na.Solve(outNALayer)
    for lyr in arcpy.mapping.ListLayers(outNALayer):
        if lyr.name == "Routes":
            arcpy.CopyFeatures_management(lyr, outRouteFile + "Scenario_2")
    arcpy.AddField_management(outRouteFile + "Scenario_2", "scenarioid", "SHORT")
    arcpy.CalculateField_management(outRouteFile + "Scenario_2", "scenarioid", 2)

    arcpy.AddMessage("Layer for Scenario_2 saved. ")
    arcpy.AddMessage(datetime.datetime.now())

    # Run with Scenario 3: Organized Smuggling 1
    arcpy.AddMessage("Running Scenario_3.")
    solverProperties = arcpy.na.GetSolverProperties(outNALayer)
    defaultRestrictions = solverProperties.restrictions
    defaultRestrictions.remove("Avoid City")
    defaultRestrictions.remove("Avoid Off-road driving")
    defaultRestrictions += ["Avoid Off-road walking"]
    defaultRestrictions.remove("Avoid On-road driving")
    defaultRestrictions.remove("Avoid Open Area")
    defaultRestrictions.remove("Prefer Ephemeral River")
    defaultRestrictions.remove("Prefer Federal Land")
    defaultRestrictions.remove("Prefer Indian Reservation")
    defaultRestrictions.remove("Prefer Northern Visibility")
    solverProperties.restrictions = defaultRestrictions
    arcpy.na.AddLocations(outNALayer, facilitiesLayerName, inFacilities,
                          fieldMappings1,"","","","","CLEAR","","","EXCLUDE")
    arcpy.na.AddLocations(outNALayer, incidentsLayerName, inIncidents,
                          fieldMappings2,"","","","","CLEAR","","","EXCLUDE")
    arcpy.AddMessage("Solving.")
    arcpy.AddMessage(datetime.datetime.now())
    arcpy.na.Solve(outNALayer)
    for lyr in arcpy.mapping.ListLayers(outNALayer):
        if lyr.name == "Routes":
            arcpy.CopyFeatures_management(lyr, outRouteFile + "Scenario_3")
    arcpy.AddField_management(outRouteFile + "Scenario_3", "scenarioid", "SHORT")
    arcpy.CalculateField_management(outRouteFile + "Scenario_3", "scenarioid", 3)
    arcpy.AddMessage("Layer for Scenario_3 saved.")
    arcpy.AddMessage(datetime.datetime.now())

    # Run with Scenario 4: Organized Smuggling 2
    arcpy.AddMessage("Running Scenario_4.")
    solverProperties = arcpy.na.GetSolverProperties(outNALayer)
    defaultRestrictions = solverProperties.restrictions
    defaultRestrictions += ["Avoid City"]
    defaultRestrictions += ["Avoid Open Area"]
    defaultRestrictions += ["Prefer Ephemeral River"]
    defaultRestrictions += ["Prefer Federal Land"]
    defaultRestrictions += ["Prefer Indian Reservation"]
    defaultRestrictions += ["Prefer Northern Visibility"]
    solverProperties.restrictions = defaultRestrictions
    arcpy.na.AddLocations(outNALayer, facilitiesLayerName, inFacilities,
                          fieldMappings1,"","","","","CLEAR","","","EXCLUDE")
    arcpy.na.AddLocations(outNALayer, incidentsLayerName, inIncidents,
                          fieldMappings2,"","","","","CLEAR","","","EXCLUDE")
    arcpy.AddMessage("Solving.")
    arcpy.AddMessage(datetime.datetime.now())
    arcpy.na.Solve(outNALayer)
    for lyr in arcpy.mapping.ListLayers(outNALayer):
        if lyr.name == "Routes":
            arcpy.CopyFeatures_management(lyr, outRouteFile + "Scenario_4")
    arcpy.AddField_management(outRouteFile + "Scenario_4", "scenarioid", "SHORT")
    arcpy.CalculateField_management(outRouteFile + "Scenario_4", "scenarioid", 4)
    arcpy.AddMessage("Layer for Scenario_4 saved.")
    arcpy.AddMessage(datetime.datetime.now())

    # Run with Scenario 5: Organized Trafficking 1
    arcpy.AddMessage("Running Scenario_5.")
    arcpy.na.AddLocations(outNALayer, facilitiesLayerName, inFacilities,
                          fieldMappings1,"","","","","CLEAR","","","EXCLUDE")
    arcpy.na.AddLocations(outNALayer, incidentsLayerName, inIncidents,
                          fieldMappings2,"","","","","CLEAR","","","EXCLUDE")
    solverProperties = arcpy.na.GetSolverProperties(outNALayer)
    defaultRestrictions = solverProperties.restrictions
    solverProperties.restrictions = defaultRestrictions
    arcpy.na.UpdateAnalysisLayerAttributeParameter(outNALayer, "Avoid City", "Restriction Usage", "AVOID_MEDIUM")
    arcpy.na.UpdateAnalysisLayerAttributeParameter(outNALayer, "Avoid Open Area", "Restriction Usage", "AVOID_MEDIUM")
    arcpy.na.UpdateAnalysisLayerAttributeParameter(outNALayer, "Prefer Ephemeral River", "Restriction Usage", "PREFER_MEDIUM")
    arcpy.na.UpdateAnalysisLayerAttributeParameter(outNALayer, "Prefer Federal Land", "Restriction Usage", "PREFER_MEDIUM")
    arcpy.na.UpdateAnalysisLayerAttributeParameter(outNALayer, "Prefer Indian Reservation", "Restriction Usage", "PREFER_MEDIUM")
    arcpy.na.UpdateAnalysisLayerAttributeParameter(outNALayer, "Prefer Northern Visibility", "Restriction Usage", "PREFER_MEDIUM")
    arcpy.AddMessage("Solving.")
    arcpy.AddMessage(datetime.datetime.now())
    arcpy.na.Solve(outNALayer)
    for lyr in arcpy.mapping.ListLayers(outNALayer):
        if lyr.name == "Routes":
            arcpy.CopyFeatures_management(lyr, outRouteFile + "Scenario_5")
    # arcpy.AddField_management(outRouteFile + "Scenario_5", "scenarioid", "SHORT")
    # arcpy.CalculateField_management(outRouteFile + "Scenario_5", "scenarioid", 5)
    arcpy.AddMessage("Layer for Scenario_5 saved.")
    arcpy.AddMessage(datetime.datetime.now())

    # Run with Scenario 6: Organized Trafficking 2
    arcpy.AddMessage("Running Scenario_6.")
    solverProperties = arcpy.na.GetSolverProperties(outNALayer)
    defaultRestrictions = solverProperties.restrictions
    solverProperties.restrictions = defaultRestrictions
    arcpy.na.UpdateAnalysisLayerAttributeParameter(outNALayer, "Avoid City", "Restriction Usage", "AVOID_LOW")
    arcpy.na.UpdateAnalysisLayerAttributeParameter(outNALayer, "Prefer Ephemeral River", "Restriction Usage", "PREFER_LOW")
    arcpy.na.AddLocations(outNALayer, facilitiesLayerName, inFacilities,
                          fieldMappings1,"","","","","CLEAR","","","EXCLUDE")
    arcpy.na.AddLocations(outNALayer, incidentsLayerName, inIncidents,
                          fieldMappings2,"","","","","CLEAR","","","EXCLUDE")
    arcpy.AddMessage("Solving.")
    arcpy.AddMessage(datetime.datetime.now())
    arcpy.na.Solve(outNALayer)
    for lyr in arcpy.mapping.ListLayers(outNALayer):
        if lyr.name == "Routes":
            arcpy.CopyFeatures_management(lyr, outRouteFile + "Scenario_6")
    # arcpy.AddField_management(outRouteFile + "Scenario_6", "scenarioid", "SHORT")
    # arcpy.CalculateField_management(outRouteFile + "Scenario_6", "scenarioid", 6)
    arcpy.AddMessage("Layer for Scenario_6 saved.")
    arcpy.AddMessage(datetime.datetime.now())

    # Run with Scenario 7: Organized Trafficking 3
    arcpy.AddMessage("Running Scenario_7.")
    solverProperties = arcpy.na.GetSolverProperties(outNALayer)
    defaultRestrictions = solverProperties.restrictions
    defaultRestrictions += ["Avoid Off-road driving"]
    solverProperties.restrictions = defaultRestrictions
    arcpy.na.AddLocations(outNALayer, facilitiesLayerName, inFacilities,
                          fieldMappings1,"","","","","CLEAR","","","EXCLUDE")
    arcpy.na.AddLocations(outNALayer, incidentsLayerName, inIncidents,
                          fieldMappings2,"","","","","CLEAR","","","EXCLUDE")
    arcpy.AddMessage("Solving.")
    arcpy.AddMessage(datetime.datetime.now()) 
    arcpy.na.Solve(outNALayer)
    for lyr in arcpy.mapping.ListLayers(outNALayer):
        if lyr.name == "Routes":
            arcpy.CopyFeatures_management(lyr, outRouteFile + "Scenario_7")
    # arcpy.AddField_management(outRouteFile + "Scenario_7", "scenarioid", "SHORT")
    # arcpy.CalculateField_management(outRouteFile + "Scenario_7", "scenarioid", 7)
    arcpy.AddMessage("Layer for Scenario_7 saved.") 
    arcpy.AddMessage(datetime.datetime.now())

except Exception as e:
    print(arcpy.GetMessages(2))
     # If an error occurred, print line number and error message
    import traceback, sys
    tb = sys.exc_info()[2]
    print(("An error occured on line %i" % tb.tb_lineno))
    print((str(e)))