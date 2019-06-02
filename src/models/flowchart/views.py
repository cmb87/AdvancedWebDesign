from flask import Blueprint, request, session, redirect, url_for, render_template, jsonify
import json

fc_blueprint = Blueprint('flowchart', __name__)


@fc_blueprint.route('/')
def flowchart():
    return render_template('flowchart/flowchartNew.html', processes=["opt_mises.py","opt_forcedResponse.py"])


@fc_blueprint.route('/operatorData', methods=['POST'])
def operatorData():
    result = []
    data = request.get_json()
    print(data.keys())
    print(data['operators'].keys())
    print(data['operatorTypes'].keys())
    with open('graph.json', 'w') as json_file:
        json.dump(data, json_file, sort_keys=True, indent=4)

    return 'Export Successfull!'

@fc_blueprint.route('/sendJson', methods=['POST'])
def sendJson():

    ang = request.args.get('fucker', 0, type=str)

    with open('graph.json') as json_file:
        data = json.load(json_file)

    return jsonify({"output" : data})


