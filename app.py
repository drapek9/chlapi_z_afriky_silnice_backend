from flask import Flask, jsonify, request


app = Flask(__name__)

import requests
from scipy.spatial import cKDTree
import numpy as np




# get_ai_response()

def silnice_min_distance(silnice_list, budovy_coords):
    """
    silnice_list: seznam silnic, každá silnice má 'geometry' -> 'coordinates'
    budovy_coords: numpy pole souřadnic budov [[x1,y1],[x2,y2],...]
    
    Vrací seznam silnic s přidanou hodnotou 'min_dist' k nejbližší budově
    """
    tree = cKDTree(budovy_coords)
    
    for s in silnice_list:
        coords = np.array(s["geometry"])
        distances, _ = tree.query(coords, k=1)
        s["min_dist"] = distances.min()  # nejbližší bod silnice k nějaké budově
    
    return silnice_list

def ahoj(silnice):
    kat_map = {
        "komunikace významná pro kraj": 3,
        "komunikace významná pro okres": 2,
        "komunikace s místním významem": 1,
        "nevýznamná komunikace": 0
    }

    stav_map = {
        "SUPERhavarijní": 5,
        "havarijní": 4,
        "nevyhovující": 3,
        "vyhovující": 2,
        "uspokojivý": 1,
        "dobrý": 0,
        "výborný": 0
    }

    trida_map = {
        "1. třída": 2,
        "2. třída": 1,
        "3. třída": 0
    }

    # výpočet priority
    for s in silnice:
        s["priority_score"] = stav_map.get(s["stav_sil"],0) + kat_map.get(s["ozn_kat"],0) + trida_map.get(s["ozn_trida"],0)

    # seřazení
    silnice_sorted = sorted(silnice, key=lambda x: x["priority_score"], reverse=False)

    # výstup
    for s in silnice_sorted:
        print(f"priorita: {s['priority_score']} - {s['stav_sil']} / {s['ozn_kat']} / {s['ozn_trida']}")
    

    import numpy as np

    url = "https://services6.arcgis.com/ogJAiK65nXL1mXAW/arcgis/rest/services/Nemocnice/FeatureServer/0/query"
    url2 = "https://services6.arcgis.com/ogJAiK65nXL1mXAW/arcgis/rest/services/Seznam_škol_a_školských_zařízení/FeatureServer/0/query"
    params = {
        "outFields": "*",
        "where": "1=1",
        "f": "geojson"
    }

    response1 = requests.get(url, params=params).json()["features"]
    response2 = requests.get(url2, params=params).json()["features"]
    
    budovy = np.array([f["geometry"]["coordinates"] for f in response1] +
                  [f["geometry"]["coordinates"] for f in response2])
    

    silnice_with_dist = silnice_min_distance(silnice, budovy)

    silnice_with_dist = sorted(silnice_with_dist, key=lambda x: x["min_dist"], reverse=True)

    for s in silnice_with_dist:
        print(f"Silnice {s.get('ozn_sil')} – min vzdálenost k budově: {s['min_dist']:.4f}")

# @app.route('/get_road_priorities_for_repair', methods=['POST'])
def get_road_priorities_for_repair():
    import requests

    url = "https://services6.arcgis.com/ogJAiK65nXL1mXAW/arcgis/rest/services/Stav_povrchu_silnic/FeatureServer/0/query"
    params = {
        "outFields": "*",
        "where": "1=1",
        "f": "geojson"
    }

    sorted_roads = []
    all_stavy = []
    all_stavy2 = []
    all_stavy3 = []

    response = requests.get(url, params=params)

    # Ověření odpovědi
    if response.status_code == 200:
        data = response.json()

        for one_feature in data["features"]:
            new_road = {}
            # if one_feature["properties"]["stav_sil"] not in ["dobrý", "výborný", "vyhovující"]: # výborný a dobrý stav nepotřebujeme opravovat
            for inf in ["ozn_sil", "ozn_trida", "stav_sil", "ozn_kat"]:
                if one_feature["properties"]["ozn_kat"] not in all_stavy:
                    all_stavy.append(one_feature["properties"]["ozn_kat"])
                if one_feature["properties"]["stav_sil"] not in all_stavy2:
                    all_stavy2.append(one_feature["properties"]["stav_sil"])
                if one_feature["properties"]["ozn_trida"] not in all_stavy3:
                    all_stavy3.append(one_feature["properties"]["ozn_trida"])
                new_road[inf] = one_feature["properties"][inf]
            new_road["geometry"] = one_feature["geometry"]["coordinates"]
            sorted_roads.append(new_road)
        ahoj(sorted_roads)
    else:
        print(f"❌ Chyba: {response.status_code}")
        # return print("neproběhlo to úspěšně")
        # return jsonify({"result": False})
    
    # return jsonify({"result": True, "data": sorted_roads})
    # return print("Vše proběhlo v pořádku")

get_road_priorities_for_repair()