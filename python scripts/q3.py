"""
Single-Day Station Travel Times: Find travel time for station Foster NB for 5-minute intervals for Sept 15, 2011. Report travel time in seconds.
"""
import pymongo 
import pandas as pd
from datetime import datetime as dt, timedelta
import datetime
  
client = pymongo.MongoClient("mongodb://35.247.52.28:27017/") 
  
# Database Name 
db = client["freeway"] 
  
# Collection Name 
col = db["StationsAndDetectors"] 
query = { "locationtext": "Foster NB"}
mydoc = col.find(query, { "detectorid": 1, "_id":0 })
mydoc1 = col.find(query, { "length": 1, "_id":0 })

for x in mydoc:
	detectors = list(x.values())
	detectors = detectors[0].strip('][').split(', ') 
	map_object = map(int, detectors)
	detectors = list(map_object)

for y in mydoc1:
 	length = y.get("length")


col1 = db["loopdata"]
new_doc = col1.find()
travel_time_sec = []
speed_arr = []
end_date = ""

for i in new_doc:
	if i.get("detectorid") in detectors:
		if "2011-09-15" in i.get("starttime"):
			if end_date == "" or end_date < i.get("starttime")[:-3]:
				if speed_arr:
					travel_time_sec.append((length / (sum(speed_arr)//len(speed_arr))) * 3600)
				time = i.get("starttime")[:-3]
				date_time_obj = dt.strptime(time, "%Y-%m-%d %H:%M:%S")
				x = date_time_obj + datetime.timedelta(minutes = 5)
				end_date = x.strftime("%Y-%m-%d %H:%M:%S")
				if i.get("speed") != None:
					print(i.get("speed"))
					speed_arr.append(i.get("speed"))
			elif end_date >= i.get("starttime")[:-3]:
				if i.get("speed") != None:
					speed_arr.append(i.get("speed"))
print(travel_time_sec)



