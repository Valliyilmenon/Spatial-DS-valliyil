import pprint as pp
import os,sys
import json
import collections

#Absolute path for Data
DIRPATH = os.path.dirname(os.path.realpath(__file__))+'/WorldData'

#Absolute path to store geojson file
DIR_PATH = os.path.dirname(os.path.realpath(__file__))+'/geo_json'

#To open and read a json file
f = open(DIRPATH+'/'+"world_cities_large.json","r")
data = f.read()
data = json.loads(data)

#A list to store formatted data
all_cities = []

for k,v in data.items():
    for j in v:
        gj = collections.OrderedDict()
        gj['type'] = "Feature"
        gj['properties'] = j
        lat = float(j['lat'])
        lon = float(j['lon'])
        del gj['properties']['lat']
        del gj['properties']['lon']
        gj["geometry"] = {}
        gj["geometry"]["type"]="Point"
        gj["geometry"]["coordinates"] = [
            lon,
            lat
            ]
        all_cities.append(gj)

#Stores only 1000 objects by deleting rest of them.
del all_cities[999:len(all_cities)-1]

out = open(DIR_PATH+'/'+"cities_gj.geojson","w")

out.write(json.dumps(all_cities, sort_keys=False,indent=4, separators=(',', ': ')))

out.close()