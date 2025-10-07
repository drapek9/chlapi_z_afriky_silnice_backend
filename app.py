from flask import Flask, jsonify, request


app = Flask(__name__)

@app.route('/get_road_priorities_for_repair', methods=['POST'])
def get_road_priorities_for_repair():
    print("Hello world, dostali jsme request na zpracování a strukturu priorit")
    return jsonify({"result": True})