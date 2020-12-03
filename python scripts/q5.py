"""
Route Finding: Find a route from Johnson Creek to Columbia Blvd on I-205 NB using the upstream and downstream fields.

"""

import pymongo
import re

client = pymongo.MongoClient("mongodb://35.247.52.28:27017/")
db = client["freeway"]
col=db["StationsAndDetectors"]

mydoc = col.find({}, {"stationid":1, "locationtext":1, "downstream":1, "_id":0})

start_point = "Johnson Cr"
end_point = "Columbia"
path = []

pattern_start = re.compile(start_point)
pattern_end = re.compile(end_point)
stationid_check = 0

#get the path from document using downstream and detectorid
for x in mydoc:
  if(all (re.search(regex, x.get("locationtext")) for regex in [start_point, "NB"])):
    path.append(x.get("locationtext"))
    stationid_check = x.get("downstream")
    continue
  if(x.get("stationid") == stationid_check):
    path.append(x.get("locationtext"))
    stationid_check = x.get("downstream")
    continue
  if(pattern_end.search(x.get("locationtext"))):
    break

#display the path  
count = 0 
path_str = "" 
for i in path:
  count = count+1
  if(count == len(path)):
    path_str = path_str + i
  else:
    path_str = path_str + i + " --> "
    
print(path_str)    
    
    
    
    
    
