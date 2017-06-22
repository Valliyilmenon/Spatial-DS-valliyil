import glob2
import os
import json

DIRPATH = os.path.dirname(os.path.realpath(__file__))+'/json_condesedfiles'
DIPATH = os.path.dirname(os.path.realpath(__file__))
# output_list = []
# read_files = glob.glob("*.json")
# for f in read_files:
#     with open(f, "rb") as infile:
#         output_list.append(json.load(infile))

# with open("merged_file.json", "wb") as outfile:
#     json.dump(output_list, outfile)

glob_data = []
print('he')
for x in glob2.glob(DIRPATH+'/'+"**.json"):
    #print(glob2.glob(DIRPATH+'/'+"**.json"))
    with open(x) as json_file:
        data = json.load(json_file)
        i = 0
        while i < len(data):
            glob_data.append(data[i])
            i += 1

f = open(DIPATH+'/'+'finalFil.json', 'w')
f.write(json.dumps(glob_data,sort_keys=True,indent=4, separators=(',', ': ')))
f.close()
# contents = []
# json_dir_name = DIRPATH + '//json_condesedfiles//file*.json'

# json_pattern = os.path.join(json_dir_name,'*.json')
# file_list = glob.glob(json_pattern)
# for file in file_list:
#     contents.append(read(file))
# print(contents)