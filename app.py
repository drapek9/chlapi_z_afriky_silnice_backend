from flask import Flask, jsonify, request


app = Flask(__name__)

@app.route('/get_road_priorities_for_repair', methods=['POST'])
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

    response = requests.get(url, params=params)

    # Ověření odpovědi
    if response.status_code == 200:
        data = response.json()

        for one_feature in data["features"]:
            new_road = {}
            if one_feature["properties"]["stav_sil"] not in ["dobrý", "výborný", "vyhovující"]: # výborný a dobrý stav nepotřebujeme opravovat
                for inf in ["ozn_trida", "typ_povrchu", "stav_sil"]:
                    if one_feature["properties"]["stav_sil"] not in all_stavy:
                        all_stavy.append(one_feature["properties"]["stav_sil"])
                    new_road[inf] = one_feature["properties"][inf]
                sorted_roads.append(new_road)
        
        print(len(sorted_roads))
        print(all_stavy)

        # for 
        # Uložení do souboru (volitelné)
    else:
        print(f"❌ Chyba: {response.status_code}")
        # return print("neproběhlo to úspěšně")
        return jsonify({"result": False})
    
    return jsonify({"result": True, "data": sorted_roads})
    # return print("Vše proběhlo v pořádku")

get_road_priorities_for_repair()