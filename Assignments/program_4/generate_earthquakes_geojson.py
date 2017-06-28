import pprint as pp
import os,sys
import json
import collections

#Absolute path for Data
DIRPATH = os.path.dirname(os.path.realpath(__file__))+'/WorldData'

#Absolute path to store geojson file
DIR_PATH = os.path.dirname(os.path.realpath(__file__))+'/geo_json'

#To open and read a json file
f = open(DIRPATH+'/'+"earthquakes-1960-2017.json","r")
data = f.read()
data = json.loads(data)

#A list to store formatted data
all_earthquakes = []

for year,value in data.items():
    for i in value:
        gj = collections.OrderedDict()
        gj['type'] = "Feature"
        gj['geometry'] = i['geometry']
        gj['properties'] = i
        lat = i['geometry']['coordinates'][0]
        lon = i['geometry']['coordinates'][1]
        del gj['properties']['geometry']

        all_earthquakes.append(gj)
        
#Stores only 1000 objects by deleting rest of them.
del all_earthquakes[999:len(all_earthquakes)-1]

out = open(DIR_PATH+'/'+"earthquake_gj.geojson","w")

out.write(json.dumps(all_earthquakes, sort_keys=False,indent=4, separators=(',', ': ')))

out.close()