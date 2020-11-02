from pymongo import MongoClient, DESCENDING
from pymongo import *
from pprint import pprint
from datetime import datetime
import requests
import json
import sys

client = MongoClient('mongodb+srv://mongo:1234@cluster0.t2irh.mongodb.net/bicycle?retryWrites=true&w=majority')
db = client.bicycle
stations = db.stations
realtime = db.vlillerealtime


# CASE 1: FIND STATION BY NAME

def find_station_by_name(partname):

    found = stations.find({"name": {"$regex": partname}})
    for elem in found:
        pprint(elem)


# CASE 2: UPDATE STATION BY ID

def update_station(statid):
    # NEW INFORMATION
    name = input("enter the new name : ")
    bike_available = input("Please enter the number of bikes available : ")
    stands_available = (input("Please enter the number of stands available : "))
    cord = [float(input("Please enter the latitude : ")), float(input("Please enter the longitude : "))]
    # Update infos
    stations.update_one({"_id": statid},
                              {'$set': {
                                  "name": name,
                                  "bike_availbale": bike_available,
                                  "stand_availbale": stands_available,
                                  "Cord": {'coordinates': cord, 'type': 'Point'}
                              }})
    print("Station updated successfully")


# CASE 3: DELETE STATION

def delete_station(statname):

    stations.delete_many({"name": {"$regex" : statname}})
    realtime.delete_many({"name": {"$regex" : statname}})
    print("Station deleted successfully")


# CASE 4 : DISABLING STATIONS

def deactivate():
    geojson_input = input("draw a polygon on geojson.io and paste the json code here:" )
    geojson_input = json.load(open(geojson_query).read().replace("\n",""))
    geojson_query = {"geo": {"$geoWithin": { "$geometry": geojson_input["features"][0]['geometry']}}}

    stations.update_many(geojson_query, {"$set": {"status": False}})

# CASE 5 : ENABLING STATIONS

def activate():
    geojson_input = input("draw a polygon on geojson.io and paste the json code here:" )
    geojson_input = json.load(open(geojson_query).read().replace("\n",""))
    geojson_query = {"geo": {"$geoWithin": { "$geometry": geojson_input["features"][0]['geometry']}}}

    stations.update_many(geojson_query, {"$set": {"status": True}})

# CASE 6 : Give all stations with a ratio bike/total_stand under 20% between 18h and 19h00 (monday to friday) :
def bike_ratio():
    stationlist = realtime.aggregate([
        {"$match": {"status": True}},
        {"$sort": {"record_timestamp": DESCENDING}},
        {"$match": {
            "$or": [
                {"$and": [{"record_timestamp": {"$lte": dateutil.parser.parse("2020-10-28 18:00:00.000Z")}},
                          {"record_timestamp": {"$gte": dateutil.parser.parse("2020-10-28 19:00:00.000Z")}}]
                 }
            ]
        }},
        {"$project":
             {"_id": "$_id",
              "name": "$name",
              "total": {"$add": ["$vlilles_dispo", "$places_dispo"]},
              "places_dispo": "$places_dispo",
              "vlilles_dispo": "$vlilles_dispo",
              "record_timestamp": "$record_timestamp"
              }},
        {"$match": {"total": {"$gt": 0}}},

        {"$project":
             {"_id": "$_id",
              "name": "$name",
              "total": "$total",
              "places_dispo": "$places_dispo",
              "vlilles_dispo": "$vlilles_dispo",
              "percent": {"$divide": ["$vlilles_dispo", "$total"]},
              "record_timestamp": "$record_timestamp"
              }},
        {"$match": {"percent": {"$lte": 0.2}}},
        {"$group":
             {"_id": "$name",
              "entries": {"$push": {
                  "percent": "$percent",
                  "places_dispo": "$places_dispo",
                  "vlilles_dispo": "$vlilles_dispo",
                  "record_timestamp": "$record_timestamp"}
              }}},
        {"$project":  
             {"_id": 1}},
    ])
    for elem in stationlist:
        print(elem["_id"])

# Test Function : 

def __main__():
    choice = True
    while choice:

        print("\n...MongoDB Velib Manager...\n ")
        print("1 : Find station by name\n")
        print("2 : Update a stations by id\n")
        print("3 : Delete a station\n")
        print("4 : Deactivate all station in an area\n")
        print("5 : Activate all station in an area\n")

        print(
            "6 : Give all stations with a ratio bike/total_stand under 20% between 18h and 19h00 (monday to friday) \n")
        print("7 : Exit\n")

        choice = int(input("\n Please enter a request "))

        if choice == 1:
            statname = input("Please enter the letters you want to find a station : ")
            find_station_by_name(statname)

        elif choice == 2:
            givenid = input("Please enter the ID of the station you want to update :")
            update_station(givenid)

        elif choice == 3:
            stats = input("Please enter the station name you want to delete : ")
            delete_station_data(stats)

        elif choice == 4:
            deactivate()
            
        elif choice == 5:
            activate()

        elif choice == 6:
            bike_ratio()

        elif choice == 7:
            print("\n The end of the Program.")
            sys.exit()

        else:
            print("\n Not a Valid Choice Try again")
            __main__()


__main__() 