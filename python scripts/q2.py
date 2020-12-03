"""
Volume: Find the total volume for the station Foster NB for Sept 15, 2011.
"""

import pymongo 

client = pymongo.MongoClient("mongodb://35.247.52.28:27017/") 
  
# Database Name 
db = client["freeway"] 
  
# Collection Name and query
col = db["StationsAndDetectors"] 
query = { "locationtext": "Foster NB" }
mydoc = col.find(query, {"detectorid": 1,"_id":0 })

detectors = []

# Get the detectors present in Forster NB station
for x in mydoc:
  detectors = list(x.values())
  detectors = detectors[0].strip('][').split(', ') 
  map_object = map(int, detectors)
  detectors = list(map_object)


print("list of detectors in Foster NB",detectors)

 
# Collection Name and query
col = db["loopdata"] 
doc2 = col.find( {"detectorid" : { "$in" : detectors }}, {"_id":0, "volume":1} )

volume = 0
temp = []

for x in doc2:
  if(len(list(x.values())) == 1):
    temp.append(list(x.values())[0])

volume = sum(temp)
  
print("total volume = ",volume)


