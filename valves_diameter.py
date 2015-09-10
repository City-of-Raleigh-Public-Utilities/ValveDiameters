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

#Make Pressure Main Feature Layer
arcpy.MakeFeatureLayer_management (pressureMain, "pMain")

#Select Valves with null diameter
arcpy.MakeFeatureLayer_management (systemValves, "sValves")
arcpy.SelectLayerByAttribute_management ("sValves", "NEW_SELECTION", " DIAMETER IS NULL ")
results = arcpy.SelectLayerByLocation_management('sValves', 'intersect', pressureMain, selection_type='SUBSET_SELECTION')

#Get Count of Null diameter valves
result = arcpy.GetCount_management(results)
count = int(result.getOutput(0))
print '%d system valves diameters are null' % count

#Create search cursor on selected valves
report = {
    "good": 0,
    "bad": 0
}

fields = ['FACILITYID', 'DIAMETER', 'SHAPE@']
with arcpy.da.SearchCursor('sValves', fields) as sCursor:
    for row in sCursor:
        point = row[2]
        arcpy.SelectLayerByLocation_management('pMain', 'intersect', point, selection_type='NEW_SELECTION')
        mainCount = int(arcpy.GetCount_management('pMain').getOutput(0))
        if mainCount > 0 and mainCount < 3:
            report['good']+=1
        else:
            report['bad']+=1

print 'Good: %d\nBad: %d' % (report['good'], report['bad'])

        # print('{0}, {1}'.format(row[0], row[1]))
