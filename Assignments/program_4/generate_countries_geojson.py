import pprint as pp
import os,sys
import json
import collections

#Absolute path for Data
DIRPATH = os.path.dirname(os.path.realpath(__file__))+'/WorldData'

#Absolute path to store geojson file
DIR_PATH = os.path.dirname(os.path.realpath(__file__))+'/geo_json'

#To open and read a json file
f = open(DIRPATH+'/'+"countries.geo.json","r")
data = f.read()
data = json.loads(data)

#A list to store formatted data
all_countries = []

for v in data:
  gj = collections.OrderedDict()
  gj = v
  all_countries.append(gj)

#Stores only 1000 objects by deleting rest of them.
del all_countries[999:len(all_countries)-1]

out = open(DIR_PATH+'/'+"countries.geojson","w")

out.write(json.dumps(all_countries, sort_keys=False,indent=4, separators=(',', ': ')))

out.close()