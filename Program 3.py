from pymongo import MongoClient, DESCENDING,GEOSPHERE
import pprint
from bson.son import SON

#Connecting to mongodb
client = MongoClient('mongodb+srv://mongo:1234@cluster0.t2irh.mongodb.net/bicycle?retryWrites=true&w=majority')
db = client.bicycle

longitude = input("Please enter your longitude:")
latitude = input("Please enter your latitude:")


#finding the closest stations, we created a geosphere index to use geospatial operators
db.vlillerealtime.create_index([("geometry", GEOSPHERE)])

closest_station = db.stations.find({"geometry" : SON([("$near", { "$geometry" : SON([("type", "Point"), ("coordinates", [float(longitude), float(latitude)])])})])})[0]

updated_station = db.vlillerealtime.find({"name": closest_station["name"],}).sort("record_timestamp",DESCENDING).next()

pprint(updated_station)