from flask import Flask, render_template, jsonify
from controllers.CommuneController import CommuneController
from helpers.JSONConverter import JSONConverter
import json

app = Flask(__name__, static_folder="../frontend/dist", template_folder='../frontend/dist')

@app.route("/")
def index():
    return render_template('index.html')

@app.route("/liste_communes")
def list_communes():
    results = CommuneController()
    return jsonify(results.get_communes())

@app.route('/geometric_matching')
def method_name():
    pass


if __name__ == "__main__":
    app.run(debug=True)

