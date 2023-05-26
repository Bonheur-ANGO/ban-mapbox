from io import StringIO
from flask import Flask, render_template, jsonify
from flask_cors import CORS
import pandas as pd
from controllers.CommuneController import CommuneController
from controllers.TronconController import TronconController
from controllers.GeometricMatchingController import GeometricMatchingController
import os
import json
import geopandas as gpd

app = Flask(__name__, static_folder="../frontend/", template_folder='../frontend/')
CORS(app)

commune_controller = CommuneController()
troncon_controller = TronconController()
geometric_matching_controller = GeometricMatchingController()

@app.route("/")
def index():
    return render_template('index.html')

@app.route("/liste_communes")
def list_communes():
    return jsonify(commune_controller.get_communes())

@app.route('/commune/<int:code_insee>')
def get_commune_by_code_insee(code_insee):
    return jsonify(commune_controller.get_commune_by_code_insee(code_insee))

@app.route('/commune/troncons/<int:code_insee>')
def get_ban_adress_by_commune(code_insee):
    return jsonify(troncon_controller.get_all_troncon(code_insee))

@app.route('/commune/voie/<int:code_insee>')
def geometric_matching(code_insee):
    return jsonify(geometric_matching_controller.getTronconsFusionned(code_insee))

@app.route('/commune/ban/<int:code_insee>')
def get_all_adress_by_commune(code_insee):
    return jsonify(commune_controller.get_all_adress_by_commune(code_insee))

@app.route('/commune/ban/jointure/<int:code_insee>')
def get_joined_adress_by_commune(code_insee):
    return jsonify(geometric_matching_controller.get_line_adress_by_voie(code_insee))

if __name__ == "__main__":
    app.run(debug=True)

