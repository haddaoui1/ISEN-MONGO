import requests
import json
from pymongo import MongoClient
import datetime
import time


#Connecting to mongodb
client = MongoClient('mongodb+srv://mongo:1234@cluster0.t2irh.mongodb.net/bicycle?retryWrites=true&w=majority')
db = client.bicycle

#fetching documents
lilleurl = "https://opendata.lillemetropole.fr/api/records/1.0/search/?dataset=vlille-realtime&q=&rows=-1"
def get_velib():
    response = requests.request("GET", lilleurl)
    response_json = json.loads(response.text.encode('utf8'))
    return response_json.get("records", [])

vlille = get_velib()

#formatting the data and adding a history timestamp
vlille_formatted = []
for velib in vlille:
    vlille_formatted.append({
        "name": velib["fields"]["nom"],
        "city": velib["fields"]["commune"],
        "vlilles_dispo": velib["fields"]["nbvelosdispo"],
        "places_dispo" : velib["fields"]["nbplacesdispo"],
        "status": velib["fields"]["etat"] == "EN SERVICE",
        "timestamp": datetime.datetime.fromisoformat(velib["record_timestamp"])})

#infinite updater loop
while True:
    print('...updating...')
    vlille = get_velib()

    # formatting the data and adding a history timestamp
    vlille_formatted = []
    for velib in vlille:
        vlille_formatted.append({
            "name": velib["fields"]["nom"],
            "city": velib["fields"]["commune"],
            "vlilles_dispo": velib["fields"]["nbvelosdispo"],
            "places_dispo": velib["fields"]["nbplacesdispo"],
            "status": velib["fields"]["etat"] == "EN SERVICE",
            "record_timestamp": datetime.datetime.fromisoformat(velib["record_timestamp"])})

    try:
        db.vlillerealtime.insert_many(vlille_formatted, ordered=False)
        print("updated successfully")
    except:
        print("update failed")
        pass

    time.sleep(10)