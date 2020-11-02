# -*- coding: utf-8 -*-
"""
Created on Mon Oct 12 09:53:23 2020

@author: ahmed haddaoui et hamza bekkari
"""

import requests
import json
from pymongo import MongoClient
from pprint import pprint

#url des apis
lilleurl = "https://opendata.lillemetropole.fr/api/records/1.0/search/?dataset=vlille-realtime&q=&rows=-1"
lyonurl = "https://download.data.grandlyon.com/ws/rdata/jcd_jcdecaux.jcdvelov/all.json"
parisurl = "https://opendata.paris.fr/api/records/1.0/search/?dataset=velib-disponibilite-en-temps-reel&q=&rows=-1"
rennesurl = "https://data.rennesmetropole.fr/api/records/1.0/search/?dataset=stations_vls&q=&lang=fr&rows=-1"


def get_velib(apiurl):
    response = requests.request("GET", apiurl)
    response_json = json.loads(response.text.encode('utf8'))
    if apiurl == lyonurl:
        return response_json.get("values", []) #special treatment for lyon's api
    else:
        return response_json.get("records", [])


#loading data into variables
vlille = get_velib(lilleurl)
vlyon = get_velib(lyonurl)
vparis = get_velib(parisurl)
vrennes = get_velib(rennesurl)

#formatting the data
vlille_formatted = []
for velib in vlille:
    vlille_formatted.append({
        "name": velib["fields"]["nom"],
        "city": velib["fields"]["commune"],
        "size": velib["fields"]["nbvelosdispo"] + velib["fields"]["nbplacesdispo"],
        "geometry": velib["geometry"],
        "TPE ": velib["fields"]["type"] != "SANS TPE",
        "status": velib["fields"]["etat"] == "EN SERVICE",
        "last update": velib["record_timestamp"] })


vparis_formatted = []
for velib in vparis:
    vparis_formatted.append({
        "name": velib["fields"]["name"],
        "city": velib["fields"]["nom_arrondissement_communes"],
        "size": velib["fields"]["capacity"],
        "geometry": velib["geometry"],
        "TPE ": False,
        "status": velib["fields"]["is_renting"] == 'OUI' and velib["fields"]["is_returning"] == 'OUI',
        "last update": velib["record_timestamp"] })

vlyon_formatted = []
for velib in vlyon:
    vlyon_formatted.append({
        "name": velib["name"],
        "city": velib["commune"],
        "size": velib["bike_stands"],
        "geometry": {"type": "Point", "coordinates": [velib["lng"], velib["lat"]]},
        "TPE ": velib["banking"],
        "status": velib["status"] == "OPEN",
        "last update": velib["last_update"] })

vrennes_formatted = []
for velib in vrennes:
    vrennes_formatted.append({
        "name": velib["fields"]["nom"],
        "city": "Rennes",
        "size": velib["fields"]["nb_socles"],
        "geometry": velib["geometry"],
        "TPE ": velib["fields"]["tpe"] == "oui",
        "status": velib["fields"]["etat"] == 'Ouverte',
        "last update": velib["record_timestamp"] })

#creating a connection instance
client = MongoClient('mongodb+srv://mongo:1234@cluster0.t2irh.mongodb.net/bicycle?retryWrites=true&w=majority')

#data wipe then insertion into the stations collection
db = client.bicycle

db.stations.delete_many({})

db.stations.insert_many(vlille_formatted)
db.stations.insert_many(vrennes_formatted)
db.stations.insert_many(vparis_formatted)
db.stations.insert_many(vlyon_formatted)
