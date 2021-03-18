from flask import Flask,render_template, request
import requests 
import plotly.graph_objects as go
from os import environ
from collections import defaultdict
from utils import api
import json

API_KEY = environ.get('API_KEY')
BASE_URL = f'https://api.openweathermap.org/data/2.5/'

app = Flask(__name__)

@app.route('/')
def main():
    plot = api.make_plot_cities(['new york', 'london','miami', 'dubai', 'los angeles'])
    return render_template('index.html', plotly_data=plot)

@app.route("/location")
def location():
    city = request.args.get('city')
    response = api.get_weather_by_location(city)
    return response

@app.route('/graph', methods=['POST'])
def graph():
    data = json.loads(request.get_data())
    cities = list(data['cities'])
    graph = api.make_plot_cities(cities)
    return graph
