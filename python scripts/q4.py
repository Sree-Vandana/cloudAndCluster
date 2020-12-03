"""
Find the average travel time for 7-9AM and 4-6PM on September 22, 2011 for the I-205 NB freeway. Report travel time in minutes.

Travel	time in minutes = ((length in miles)/avg(speed in miles per hour))*(60minutes/hour)	
"""
import pymongo 
from datetime import datetime as dt, timedelta
import datetime
 
client = pymongo.MongoClient("mongodb://35.247.52.28:27017/") 

# Database Name 
db = client["freeway"]

# Collection Name 
col = db["StationsAndDetectors"] 

query = {
"locationtext": {
"$regex": 'I-205 NB',
"$options" :'i' # case-insensitive
}
}

mydoc = col.find(query, { "detectorid": 1, "_id":0 })
mydoc1 = col.find(query, { "length": 1, "_id":0 })

detectors = []
all_detectors=[]	#to store detectors as [[],[],[]]
all_detectors_un=[]	# to store detectors as [,..,]

for x in mydoc:
  detectors = list(x.values())
  detectors = detectors[0].strip('][').split(', ') 
  map_object = map(int, detectors)
  detectors = list(map_object)
  all_detectors.append(detectors)
  #all detecor id's unnested
  for i in detectors:
    all_detectors_un.append(i)
  
print("detectors list ",all_detectors_un)
length=[]
for y in mydoc1:
 	length.append(y.get("length"))
print("length = ",length)

col1 = db["loopdata"]

query1 = {"$and": [{"detectorid":{"$in":all_detectors_un}}, 
			 {"starttime": {
					"$regex": '2011-09-22',
					"$options" :'i' # case-insensitive
					}}]}
					
new_doc = col1.find(query1,{ "detectorid": 1, "_id":0, "speed":1, "starttime":1 })

start_datetime_1 = "2011-09-22 7:00:00"
end_datetime_1 = "2011-09-22 9:00:00"

start_datetime_2 = "2011-09-22 14:00:00"
end_datetime_2 = "2011-09-22 16:00:00"

new_dict_1 = {}
new_dict_2 = {}

for x in new_doc:
  key = x.get('detectorid')
  time = x.get("starttime")[:-3]
  date_time_obj = dt.strptime(time, "%Y-%m-%d %H:%M:%S")
  
  if(date_time_obj >= dt.strptime(start_datetime_1, "%Y-%m-%d %H:%M:%S") and date_time_obj <= dt.strptime(end_datetime_1, "%Y-%m-%d %H:%M:%S")):
    if("speed" in x): 
      if(key in new_dict_1):
        new_dict_1[key].append(x.get('speed'))  
      else:
        new_dict_1[key] = [x.get('speed')]
        
  if(date_time_obj >= dt.strptime(start_datetime_2, "%Y-%m-%d %H:%M:%S") and date_time_obj <= dt.strptime(end_datetime_2, "%Y-%m-%d %H:%M:%S")):
    if("speed" in x): 
      if(key in new_dict_2):
        new_dict_2[key].append(x.get('speed'))  
      else:
        new_dict_2[key] = [x.get('speed')]

travel_time=[]
list_of_dict = [new_dict_1, new_dict_2]

#avg speed for each detector using new_dict_1 dictinary
avg_speed_each_detector=[]

for index in range(len(list_of_dict)):
  for i in all_detectors:
    li=[]
    for j in i:
      print(list_of_dict[index].get(j))
      if(list_of_dict[index].get(j) != None):
        l=len(list_of_dict[index].get(j))
        total = sum(list_of_dict[index].get(j))
        li.append(total/l)
      
    avg_speed_each_detector.append(li)
  
  print("Avg Speed of each Detector\n",avg_speed_each_detector)
  #for each station
  avg_speed_each_station=[]

  for k in avg_speed_each_detector:
    if(len(k)!=0):
      total=sum(k)
      avg=total/len(k)
      avg_speed_each_station.append(avg)

  print("Average Speed of each Station\n",avg_speed_each_station)

  avg_speed = sum(avg_speed_each_station)/len(avg_speed_each_station)
  print("avg_speed = ", avg_speed)
  avg_len = sum(length)/len(length)
  print("avg_len = ", avg_len)

  travel_time.append(((avg_len)/(avg_speed))*60)
  
print("avg travel time between 7 to 9 and 4 to 6 is ",travel_time, "mintues")
print("avgerage travel time = ", sum(travel_time)/len(travel_time), " mintues")








