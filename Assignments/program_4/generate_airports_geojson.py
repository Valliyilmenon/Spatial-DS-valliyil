import pprint as pp
import os,sys
import json
import string
import collections

#Absolute path for Data
DIRPATH = os.path.dirname(os.path.realpath(__file__))+'/WorldData'

#Absolute path to store geojson file
DIR_PATH = os.path.dirname(os.path.realpath(__file__))+'/geo_json'

#To open and read a json file
f = open(DIRPATH+'/'+"airports.json","r")
data = f.read()
data = json.loads(data)

#A list to store formatted data
all_airports = []

for k,v in data.items():
    gj = collections.OrderedDict()
    gj['type'] = "Feature"
    gj['properties'] = v
    lat = v['lat']
    lon = v['lon']
    del gj['properties']['lat']
    del gj['properties']['lon']
    gj["geometry"] = {}
    gj["geometry"]["type"]="Point"
    gj["geometry"]["coordinates"] = [
          lon,
          lat
        ]
    all_airports.append(gj)

#Stores only 1000 objects by deleting rest of them.
del all_airports[999:len(all_airports)-1]

out = open(DIR_PATH+'/'+"airports_gj.geojson","w")

out.write(json.dumps(all_airports, sort_keys=False,indent=4, separators=(',', ': ')))

out.close()