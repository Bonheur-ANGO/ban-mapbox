from flask import Flask, render_template
import json

app = Flask(__name__, static_folder="../frontend/dist", template_folder='../frontend/dist')

@app.route("/")
def index():
    return render_template('index.html')

if __name__ == "__main__":
    app.run(debug=True)

