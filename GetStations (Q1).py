# -*- coding: utf-8 -*-
"""
Created on Mon Oct 12 09:53:23 2020

@author: ahmed haddaoui et hamza bekkari
"""

import requests
import json
from pprint import pprint

def get_vlille():
    url = "https://opendata.lillemetropole.fr/api/records/1.0/search/?dataset=vlille-realtime&q=&rows=300&facet=libelle&facet=nom&facet=commune&facet=etat&facet=type&facet=etatconnexion"

    pload = {}
    headers= {}

    response=requests.request("GET", url, headers=headers, data=pload)

    response_json = json.loads(response.text.encode('utf8'))

    return response_json.get("records",[])

Vlille= get_vlille()

for vlille in Vlille:
    pprint(vlille)

#get stations
#Lille

def get_vlille():
    
    url = "https://opendata.lillemetropole.fr/api/records/1.0/search/?dataset=vlille-realtime&q=&rows=300&facet=libelle&facet=nom&facet=commune&facet=etat&facet=type&facet=etatconnexion"
    payload = {}
    headers= {}
    response = requests.request("GET", url, headers=headers, data = payload)
    response_json = json.loads(response.text.encode('utf8'))
    return response_json.get("records", [])

Vlille = get_vlille()
for vlille in vlilles:
    pprint(vlille)


    
#lyon


def get_vlyon():
    key="2f3f00af9ce4e0959c3611b330a7be5f1af2b436"
    url = "https://api.jcdecaux.com/vls/v3/stations?contract=Lyon&apiKey=2f3f00af9ce4e0959c3611b330a7be5f1af2b436"
    payload = {}
    headers= {}
    response = requests.request("GET", url, headers=headers, data = payload)
    response_json = json.loads(response.text.encode('utf8'))
    return response_json
Vlille = get_vlyon()
for vlille in vlilles:
    pprint(vlille)
    
    

#paris

def get_vparis():
    url = "https://opendata.paris.fr/api/records/1.0/search/?dataset=velib-disponibilite-en-temps-reel&q=&rows=2971&facet=name&facet=is_installed&facet=is_renting&facet=is_returning&facet=nom_arrondissement_communes"
    payload = {}
    headers= {}
    response = requests.request("GET", url, headers=headers, data = payload)
    response_json = json.loads(response.text.encode('utf8'))
    return response_json.get("records", [])
Vlille = get_vparis()
for vlille in vlilles:
    pprint(vlille)
    
 
    
#rennes   


def get_vrennes():
    url = "https://data.rennesmetropole.fr/api/records/1.0/search/?dataset=etat-des-stations-le-velo-star-en-temps-reel&q=&rows=9969&facet=nom&facet=etat&facet=nombreemplacementsactuels&facet=nombreemplacementsdisponibles&facet=nombrevelosdisponibles"
    payload = {}
    headers= {}
    response = requests.request("GET", url, headers=headers, data = payload)
    response_json = json.loads(response.text.encode('utf8'))
    return response_json.get("records", [])
Vlilles = get_vrennes()
for vlille in vlilles:
    pprint(vlille)

    
    