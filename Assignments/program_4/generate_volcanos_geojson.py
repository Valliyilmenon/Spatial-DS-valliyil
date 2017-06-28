import pprint as pp
import os,sys
import json
import collections

#Absolute path for Data
DIRPATH = os.path.dirname(os.path.realpath(__file__))+'/WorldData'

#Absolute path to store geojson file
DIR_PATH = os.path.dirname(os.path.realpath(__file__))+'/geo_json'

#To open and read a json file
f = open(DIRPATH+'/'+"world_volcanos.json","r")
data = f.read()
data = json.loads(data)

#A list to store formatted data
all_volcanos = []

for volcano in data:
    gj = collections.OrderedDict()
    gj['type'] = "Feature"
    gj['properties'] = volcano
    try:
        lat = float(volcano['Lat'])
        lon = float(volcano['Lon'])
    except:
        pass
    del gj['properties']['Lat']
    del gj['properties']['Lon']
    gj["geometry"] = {}
    gj["geometry"]["type"]="Point"
    gj["geometry"]["coordinates"] = [
        lon,
        lat
            ]
    all_volcanos.append(gj)

#Stores only 1000 objects by deleting rest of them.
del all_volcanos[999:len(all_volcanos)-1]

out = open(DIR_PATH+'/'+"volcano.geojson","w")

out.write(json.dumps(all_volcanos, sort_keys=False,indent=4, separators=(',', ': ')))

out.close()