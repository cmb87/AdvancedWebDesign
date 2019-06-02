from flask import Blueprint, request, session, redirect, url_for, render_template, jsonify
from src.models.geometry.cube import Cube

webgl_blueprint = Blueprint('webgl', __name__)


# https://www.tutorialspoint.com/webgl/webgl_cube_rotation.htm
# https://www.tutorialspoint.com/webgl/webgl_drawing_a_model.htm

@webgl_blueprint.route('/')
def webglcube():
    return render_template('webgl/cube.html')


@webgl_blueprint.route('/webgltriangle')
def webgltriangle():
    return render_template('webgl/triangle.html')


@webgl_blueprint.route('/webglstl')
def webglstl():
    cube = Cube()
    vertices, nvertices, color = cube.readSTL()

    return render_template('webgl/stlNew.html', geometry=vertices, npoints=nvertices, color=color)


@webgl_blueprint.route('/starfield')
def starfield():
	return render_template('starfield/starfield.html')