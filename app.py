from flask import Flask, jsonify, request


app = Flask(__name__)

@app.route('/get_road_priorities_for_repair', methods=['POST'])
def get_road_priorities_for_repair():
    print("Hello world, dostali jsme request na zpracování a strukturu priorit")
    all_data = request.get_json()

    stavy_silnic = all_data.get("stavy_silnic")
    historie_oprav_silnic = all_data.get("historie_oprav_silnic")

    if stavy_silnic == None or historie_oprav_silnic == None:
        return jsonify({"result": False, "reason": "server nezískal požadovaná data"})
    
    print("------------------ stavy silnic -------------------")
    print(stavy_silnic)
    print("------------------ historie oprav silnic -------------------")
    print(historie_oprav_silnic)
    
    return jsonify({"result": True})