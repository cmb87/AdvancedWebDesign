import sys
import os
from flask import Flask, render_template, url_for
from stl import mesh
import json

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '../'))

from src.models.geometry.cube import Cube

app = Flask(__name__)
app.secret_key = "123"

#@app.before_first_request
# def init_db():
#    Database.initialize()


@app.route('/')
def home():
    return render_template('starfield/starfield.html')


# https://www.tutorialspoint.com/d3js/d3js_concepts.htm
@app.route('/d3basic')
def d3basic():
    return render_template('d3/basic.html')

# https://www.tutorialspoint.com/webgl/webgl_cube_rotation.htm
# https://www.tutorialspoint.com/webgl/webgl_drawing_a_model.htm


@app.route('/webglcube')
def webglcube():
    return render_template('webgl/cube.html')


@app.route('/webgltriangle')
def webgltriangle():
    return render_template('webgl/triangle.html')


@app.route('/webgllines')
def webgllines():
    cube = Cube()
    vertices, nvertices, color = cube.readSTL()

    return render_template('webgl/plane.html', geometry=vertices, npoints=nvertices, color=color)


if __name__ == '__main__':
    app.run()
