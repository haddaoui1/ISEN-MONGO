import requests
import json
from pprint import pprint
from pymongo import MongoClient


clients = MongoClient('mongodb://localhost:27017/')
db = clients.vls 
collection_Vlille = db.Vlille  

def get_velib(url):
    payload = {}
    headers = {}
    response = requests.request("GET", url, headers=headers, data=payload)
    response_json = json.loads(response.text.encode('utf8'))
    return response_json.get("records", [])
Vlille = get_velib("https://opendata.lillemetropole.fr/api/records/1.0/search/?dataset=vlille-realtime&q=&rows=-1")

Vlille_format= []
for vlib in Vlille:
    Vlille_format.append({
        "name": vlib["fields"]["nom"],
        "vlilles_dispo": vlib["fields"]["nbvelosdispo"],
        "places_dispo" : vlib["fields"]["nbplacesdispo"],
        "status": vlib["fields"]["etat"] == "EN SERVICE",
        "record_timestamp": vlib["record_timestamp"] })
    
print("inserted : " + str(len(collection_Vlille.insert_many(Vlille_format).inserted_ids)))