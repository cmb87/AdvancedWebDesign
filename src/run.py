import sys
import os
from flask import Flask, render_template, url_for, request, jsonify
from flask_dropzone import Dropzone
from stl import mesh
import json
import numpy as np

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '../'))

from src.common.database import Database
import src.config as config

app = Flask(__name__)
app.secret_key = "123"

### Dropzone settings ###
basedir = os.path.abspath(os.path.dirname(__file__))


app.config.update(
    UPLOADED_PATH=os.path.join(basedir, 'uploads'),
    # Flask-Dropzone config:
    # DROPZONE_ALLOWED_FILE_TYPE='image',
    DROPZONE_MAX_FILE_SIZE=3e+5,
    DROPZONE_MAX_FILES=30,
    DROPZONE_IN_FORM=True,
    DROPZONE_UPLOAD_ON_CLICK=True,
    DROPZONE_UPLOAD_ACTION='data.handle_upload',  # URL or endpoint
    DROPZONE_UPLOAD_BTN_ID='submit',
    DROPZONE_TIMEOUT=25 * 60 * 1000,
)

dropzone = Dropzone(app)

### Init DB ###

@app.before_first_request
def init_db():
    """Create database and tables
    """
    tables = {config.USERCOLLECTION: {"id": "INTEGER PRIMARY KEY AUTOINCREMENT", "email": "TEXT", "password": "TEXT"},
              'progress': {"id": "INTEGER PRIMARY KEY AUTOINCREMENT", "task_id": "INT", "progress": "FLOAT"},
              'tasks': {"id": "INTEGER PRIMARY KEY AUTOINCREMENT", "user_id": "INT", "name": "TEXT"},
              }
    for table, columns in tables.items():
        Database.delete_table(table)
        Database.create_table(table, columns)


@app.route('/')
def home():
    return render_template('home.html')


@app.route('/vis')
def vis_example():
    return render_template('vis/vis_example.html')

@app.route('/vis2')
def vis_example2():
    return render_template('vis/vis_example2.html')

from src.models.users.views import user_blueprint
from src.models.d3.views import d3_blueprint
from src.models.geometry.views import webgl_blueprint
from src.models.flowchart.views import fc_blueprint
from src.models.data.views import data_blueprint
from src.models.bokeh.views import bokeh_blueprint

app.register_blueprint(user_blueprint, url_prefix="/users")
app.register_blueprint(d3_blueprint, url_prefix="/d3")
app.register_blueprint(webgl_blueprint, url_prefix="/webgl")
app.register_blueprint(fc_blueprint, url_prefix="/flowchart")
app.register_blueprint(data_blueprint, url_prefix="/data")
app.register_blueprint(bokeh_blueprint, url_prefix="/bokeh")

if __name__ == '__main__':
    app.run()
