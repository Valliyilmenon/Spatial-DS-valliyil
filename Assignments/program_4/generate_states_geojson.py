import pprint as pp
import os,sys
import json
import collections

#Absolute path for Data
DIRPATH = os.path.dirname(os.path.realpath(__file__))+'/WorldData'

#Absolute path to store geojson file
DIR_PATH = os.path.dirname(os.path.realpath(__file__))+'/geo_json'

#To open and read a json file
f = open(DIRPATH+'/'+"state_borders.json","r")
data = f.read()
data = json.loads(data)

#A list to store formatted data
all_states = []

for states in data:
    gj = collections.OrderedDict()
    gj['type'] = "Feature"
    gj['properties'] = states
    borders = states['borders']
    del gj['properties']['borders']
    gj["geometry"] = {}
    gj["geometry"]["type"]="Polygon"
    gj["geometry"]["coordinates"] = borders   
    all_states.append(gj)

out = open(DIR_PATH+'/'+"states.geojson","w")

out.write(json.dumps(all_states, sort_keys=False,indent=4, separators=(',', ': ')))

out.close()