from flask import Blueprint, request, session, redirect, url_for, render_template, jsonify
import numpy as np

d3_blueprint = Blueprint('d3', __name__)

# D3 stuff
# https://www.tutorialspoint.com/d3js/d3js_concepts.htm
@d3_blueprint.route('/')
def d3basic():
    return render_template('d3/basic.html')


@d3_blueprint.route('/contour')
def d3contourplot():
    return render_template('d3/contourplot.html')


@d3_blueprint.route('/getDataContour', methods=['GET', 'POST'])
def sendDataContour():
    if request.method == 'POST':

        def f(x, y):
            return np.sin(x) ** 10 + np.cos(10 + y * x) * np.cos(x)

        x = np.linspace(0, 5, 50)
        y = np.linspace(0, 5, 40)

        X, Y = np.meshgrid(x, y)
        X, Y = X.flatten(), Y.flatten()
        Z = f(X, Y)

        levels = np.linspace(Z.min(), Z.max(), 11).tolist()
        data = []
        for x, y, z in zip(X.tolist(), Y.tolist(), Z.tolist()):
            data.append({"x": x, "y": y, "z": z})

        return jsonify(values=data, width=800, height=200, levels=levels)

    else:
        return "Aint workin"

@d3_blueprint.route('/getData', methods=['GET', 'POST'])
def sendData():
    if request.method == 'POST':

        X = np.linspace(0, 5, 40)
        Y = np.sin(X)
        Z = np.sin(X)

        data = []
        for x, y, z in zip(X.tolist(), Y.tolist(), Z.tolist()):
            data.append({"x": x, "y": y, "z": z})

        return jsonify(values=data, width=800, height=200)

    else:
        return "Aint workin"

@d3_blueprint.route('/line')
def d3line():
    return render_template('d3/line.html')