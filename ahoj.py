from scipy.spatial import cKDTree
from shapely.geometry import Point, LineString
import numpy as np

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

# --- příklad použití ---
# načti budovy (nemocnice+školy)
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
else:
    print(f"❌ Chyba: {response.status_code}")

url_nemocnice = "https://services6.arcgis.com/ogJAiK65nXL1mXAW/arcgis/rest/services/Nemocnice/FeatureServer/0/query"
url_skoly = "https://services6.arcgis.com/ogJAiK65nXL1mXAW/arcgis/rest/services/Seznam_škol_a_školských_zařízení/FeatureServer/0/query"
params = {"outFields":"*","where":"1=1","f":"geojson"}

resp_n = requests.get(url_nemocnice, params=params).json()
resp_s = requests.get(url_skoly, params=params).json()

budovy = np.array([f["geometry"]["coordinates"] for f in resp_n["features"]] +
                  [f["geometry"]["coordinates"] for f in resp_s["features"]])

# silnice_list = [{"geometry":{"coordinates":[[x1,y1],[x2,y2],...]}}, ...]
silnice_with_dist = silnice_min_distance(sorted_roads, budovy)

# výpis
silnice_with_dist = sorted(silnice_with_dist, key=lambda x: x["min_dist"], reverse=True)

for s in silnice_with_dist:
    print(f"Silnice {s.get('ozn_sil')} – min vzdálenost k budově: {s['min_dist']:.4f}")