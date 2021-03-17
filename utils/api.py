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
    by_city = f'forecast?units=imperial&q={city_name.lower()}&appid={API_KEY}'
    response = requests.get(BASE_URL + by_city)
    return response.json()

def get_forecast_by_cities(cities):
    responses = {}
    for city in cities:
        response = get_forecast_by_city(city)
        responses[city] = response
    return responses

def get_weather_by_location(city):
    location_search = f'weather?&units=imperial&q={city}&appid={API_KEY}'
    response = requests.get(BASE_URL + location_search)
    return response.json()

def make_plot_cities(cities):
    data = get_forecast_by_cities(cities)
    dates = []
    city_to_temp = defaultdict(list)
    city_to_humidity = defaultdict(list)
    city_to_feels = defaultdict(list)
    city_to_pressure = defaultdict(list)
    city_to_min_temp = defaultdict(list)

    fig = go.Figure(layout_title_text="Max Temp", 
    layout = {'xaxis': {'title': '5 Day Overview', 
                        'visible': True, 
                        'showticklabels': True}, 
            'yaxis': {'title': 'Degrees Fahrenheit', 
                        'visible': True, 
                        'showticklabels': True}
            })

    fig.data = []
    
    
    for city, infor in data.items():
        name = city.lower()
        for item in infor['list']:
            #res[name].append(item['main'][])
            city_to_temp[name].append(item['main']['temp_max'])
            city_to_humidity[name].append(item['main']['humidity'])
            city_to_feels[name].append(item['main']['feels_like'])
            city_to_pressure[name].append(item['main']['pressure'])
            city_to_min_temp[name].append(item['main']['temp_min'])
            dates.append(item['dt_txt'])


    for i, data_map in enumerate([city_to_temp, city_to_humidity,  city_to_feels, city_to_pressure, city_to_min_temp]):
        for city in cities:
            if i != 0:
                fig.add_trace(go.Scatter(x=dates, y=data_map[city.lower()], mode='lines', name=city, visible=False))
            else:
                fig.add_trace(go.Scatter(x=dates, y=data_map[city.lower()], mode='lines', name=city, visible=True))
            
    fig.update_layout(
    updatemenus=[go.layout.Updatemenu(
        active=0,
        buttons=list(
            [dict(method='update', label='Max Temp', args = [{'visible': [True, True, True, True, True, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False]},
                        {'title': 'Max Temp',
                            'showlegend':True,
                            'yaxis':{'title':'Degrees Farenheit', 
                            'visible': True, 
                            'showticklabels': True}
                        }]),
            dict(method='update', label='Feels Like', args = [{'visible': [False, False, False, False, False,False, False, False, False, False, True, True, True, True, True, False, False, False, False, False, False, False, False, False, False]},
                        {'title': 'Feels Like',
                            'showlegend':True,
                            'yaxis':{'title':'Degrees Farenheit', 
                            'visible': True, 
                            'showticklabels': True}
                        }]), 
            dict(method='update', label='Humidity', args = [{'visible': [False, False, False, False, False, True, True, True, True, True, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False]},
                        {'title': 'Humidity',
                            'showlegend':True, 
                            'yaxis':{'title':'Percentage', 
                            'visible': True, 
                            'showticklabels': True}
                        }]), 
            dict(method='update', label='Pressure', args = [{'visible': [False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, True, True, True, True, True, False, False, False, False,False]},
                        {'title': 'Pressure',
                        'showlegend':True, 
                        'yaxis':{'title':'Milibars (mb)', 
                        'visible': True, 
                        'showticklabels': True}
                        }]), 
            dict(method='update', label='Min Temp', args = [{'visible': [False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, True, True, True, True, True]},
                        {'title': 'Min Temp',
                        'showlegend':True, 
                        'yaxis':{'title':'Degrees Farenheit', 
                        'visible': True, 
                        'showticklabels': True}
                        }]), 
            ]),
        )
    ])
    
    fig_json = fig.to_json()
    return fig_json
    '''
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
    '''