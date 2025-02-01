import flask
from flask_cors import CORS
from flask import request, jsonify, render_template
from movies import get_similar, get_recommendations
import pandas as pd

app = flask.Flask(__name__)
CORS(app, resources={r"/*": {"origins": "http://localhost:8010"}})

@app.route('/')
def home():
    return render_template('index.html')


@app.route('/similar', methods=['POST'])
def similar():
    title = request.form['title']
    recommendations = get_recommendations(title)
    if isinstance(recommendations, pd.Series):
        recommendations = recommendations.tolist()
    return jsonify(recommendations)


if __name__ == '__main__':
    app.run()
