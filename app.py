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
            sorted_roads.append(new_road)
        # print(data["features"])
        # print(sorted_roads)
        print(all_stavy)
        print(all_stavy2)
        print(all_stavy3)

        # ahoj(sorted_roads)

        # get_ai_response(sorted_roads)

        # ozn_trida, typ_povrchu, stav_sil

        # for 
        # Uložení do souboru (volitelné)
    else:
        print(f"❌ Chyba: {response.status_code}")
        # return print("neproběhlo to úspěšně")
        return jsonify({"result": False})
    
    return jsonify({"result": True, "data": sorted_roads})
    # return print("Vše proběhlo v pořádku")

# get_road_priorities_for_repair()