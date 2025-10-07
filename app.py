from flask import Flask, jsonify, request


app = Flask(__name__)


@app.route('/get_all_road_data', methods=['POST'])
def all_road_data():
    print("Hello world, dostali jsme request na zpracování a strukturu všech dat")
    return jsonify({"result": True})

@app.route('/get_road_priorities_for_repair', methods=['POST'])
def all_road_data():
    print("Hello world, dostali jsme request na zpracování a strukturu priorit")
    return jsonify({"result": True})