"""
Update: Change the milepost of the Foster NB station to 22.6.
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

mydoc_milepost = col.find(query, { "milepost": 1, "_id":0 })
for m in mydoc_milepost:
	col.update_one({"milepost":m.get("milepost")},{"$set":{"milepost":22.6}})
