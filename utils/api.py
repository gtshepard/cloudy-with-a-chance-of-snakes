import requests 
import plotly.graph_objects as go
from os import environ
from collections import defaultdict

API_KEY = environ.get('API_KEY')
BASE_URL = f'https://api.openweathermap.org/data/2.5/'

def get_forecast_by_location(lat, lon):
    location_search_weeks = f'forecast?units=imperial&lat={lat}&lon={lon}&appid={API_KEY}'
    response = requests.get(BASE_URL + location_search_weeks)
    return response.json()

def get_forecast_by_city(city_name):
    by_city = f'forecast?units=imperial&q={city_name}&appid={API_KEY}'
    response = requests.get(BASE_URL + by_city)
    return response.json()

def get_forecast_by_cities(cities):
    responses = {}
    for city in cities:
        response = get_forecast_by_city(city)
        responses[city] = response
    return responses

def get_weather_by_location(city):
    location_search = f'weather?q={city}&appid={API_KEY}'
    response = requests.get(BASE_URL + location_search)
    return response.json()

def make_plot_cities(cities, option):
    data = get_forecast_by_cities(cities)
    res = defaultdict(list)
    mapOption = {'temp_min':'Minimum Temperature', 'temp_max':"Maximum Temperature", 'pressure': "Pressure", 'humidity': "Humidity"}
    dates = []
    
    for city, infor in data.items():
        name = city.lower()
        for item in infor['list']:
            res[name].append(item['main'][option])
            dates.append(item['dt_txt'])

    fig = go.Figure()
    for city in cities:
        fig.add_trace(go.Scatter(x=dates, y=res[city.lower()], mode='lines', name=city))
        
    fig.update_layout(title=f"{mapOption[option]}'s forecast", yaxis={'title':f'{mapOption[option]}'}, xaxis={'title':'Date'})
    fig_json = fig.to_json()
    
    return fig_json