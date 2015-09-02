#mdule: valves_diameter.py
#author: Coery White
#description: Adds diameters to wSystemValves and wControlValves that have diameter set to null

import arcpy
import os
import sys

#Sets workspace
arcpy.env.workspace = os.path.join(os.path.dirname(sys.argv[0]), 'RPUD.gdb')

#Set varibles
systemValves = 'wSystemValve'
contorlValves = 'wControlValve'
pressureMain = 'wPressureMain'

#Select Valves with null diameter
arcpy.MakeFeatureLayer_management (systemValves, "sValves")
arcpy.SelectLayerByAttribute_management ("sValves", "NEW_SELECTION", " DIAMETER IS NULL ")
results = arcpy.SelectLayerByLocation_management('sValves', 'intersect', pressureMain, selection_type='SUBSET_SELECTION')

#Get Count of Null diameter valves
result = arcpy.GetCount_management(results)
count = int(result.getOutput(0))
print '%d system valves diameters are null' % count

#Create search cursor on selected valves
fields = ['FACILITYID', 'DIAMETER']
with arcpy.da.SearchCursor('sValves', fields) as sCursor:
    for row in sCursor:
        print('{0}, {1}'.format(row[0], row[1]))
