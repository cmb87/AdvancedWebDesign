import sys
import os
from flask import Flask, render_template, url_for, request, jsonify
from stl import mesh
import json
import numpy as np

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '../'))

from src.common.database import Database
import src.models.users.constants as UserConstants

app = Flask(__name__)
app.secret_key = "123"


@app.before_first_request
def init_db():
    """Create database and tables
    """
    tables = {UserConstants.COLLECTION: {"id": "INTEGER PRIMARY KEY AUTOINCREMENT", "email": "TEXT", "password": "TEXT"},
              'progress': {"id": "INTEGER PRIMARY KEY AUTOINCREMENT", "task_id": "INT", "progress": "FLOAT"},
              'tasks': {"id": "INTEGER PRIMARY KEY AUTOINCREMENT", "user_id": "INT", "name": "TEXT"},
              }
    for table, columns in tables.items():
        Database.delete_table(table)
        Database.create_table(table, columns)


@app.route('/')
def home():
    return render_template('home.html')


from src.models.users.views import user_blueprint
from src.models.d3.views import d3_blueprint
from src.models.geometry.views import webgl_blueprint
from src.models.flowchart.views import fc_blueprint

app.register_blueprint(user_blueprint, url_prefix="/users")
app.register_blueprint(d3_blueprint, url_prefix="/d3")
app.register_blueprint(webgl_blueprint, url_prefix="/webgl")
app.register_blueprint(fc_blueprint, url_prefix="/flowchart")



if __name__ == '__main__':
    app.run()
