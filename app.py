from flask import Flask,render_template
import requests 
import plotly.graph_objects as go
from os import environ, path
from dotenv import load_dotenv
from collections import defaultdict

API_KEY = environ.get('API_KEY')
BASE_URL = f'https://api.openweathermap.org/data/2.5/'

#import geocoder
#g = geocoder.ip('me')
#print(g.latlng)

app = Flask(__name__)

@app.route("/")
def hello():     
    make_city_weather_plot()
    return render_template('new_plot.html')

'''
@app.route("/data")
def see_data():
    #response = get_weather_by_location('42.54149775840134','-75.01959026744706' )
    #print(response['list'][0][''])
    response = get_weather_for_city('los angeles')
    return response
'''
'''
def get_weather_by_location(lat, lon):
    location_search = f'weather?lat={lat}&lon={lon}&appid={API_KEY}'
    location_search_weeks = f'forecast?&units=imperial&lat={lat}&lon={lon}&appid={API_KEY}'

    response = requests.get(BASE_URL + location_search_weeks)
    return response.json()
'''

def get_weather_for_city(city_name):
    by_city = f'forecast?&units=imperial&q={city_name}&appid={API_KEY}'
    response = requests.get(BASE_URL + by_city)
    return response.json()

def get_weather_for_cities(cities):
    responses = []
    for city in cities:
        response = get_weather_for_city(city)
        responses.append(response)
    return responses


def make_city_weather_plot(cities =['new york', 'london','miami', 'dubai', 'los angeles']):
    #cities = ['new york', 'london','miami', 'dubai', 'los angeles']
    data = get_weather_for_cities(cities)
    city_to_temp = defaultdict(list)
    city_to_humidity = defaultdict(list)
    city_to_feels = defaultdict(list)
    city_to_pressure = defaultdict(list)
    city_to_min_temp = defaultdict(list)

    fig = go.Figure(layout_title_text="Max Temp", 
    layout = {'xaxis': {'title': '5 Day Span', 
                        'visible': True, 
                        'showticklabels': False}, 
              'yaxis': {'title': 'Degrees Fahrenheit', 
                        'visible': True, 
                        'showticklabels': True}
              })


    dates = set()
    for city in data:
        name = city['city']['name'].lower()
        for time_interval in city['list']:
            dates.add(time_interval['dt_txt'])
            print(time_interval['main']['temp_max'])
            city_to_temp[name].append(time_interval['main']['temp_max'])
            city_to_humidity[name].append(time_interval['main']['humidity'])
            city_to_feels[name].append(time_interval['main']['feels_like'])
            city_to_pressure[name].append(time_interval['main']['pressure'])
            city_to_min_temp[name].append(time_interval['main']['temp_min'])

    for city in cities:
        fig.add_trace(go.Scatter(x=[i for i in range(120)], y=city_to_temp[city], mode='lines', name=city))

    for city in cities:
        fig.add_trace(go.Scatter(x=[i for i in range(120)], y=city_to_humidity[city], mode='lines', name=city, visible=False))
    
    for city in cities:
        fig.add_trace(go.Scatter(x=[i for i in range(120)], y=city_to_feels[city], mode='lines', name=city, visible=False))

    for city in cities:
        fig.add_trace(go.Scatter(x=[i for i in range(120)], y=city_to_pressure[city], mode='lines', name=city, visible=False))

    for city in cities:
        fig.add_trace(go.Scatter(x=[i for i in range(120)], y=city_to_min_temp[city], mode='lines', name=city, visible=False))

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
    # a simple HTML template
    template = """<html>
    <head>
        <script src="https://cdn.plot.ly/plotly-latest.min.js"></script>
    </head>
    <body>
        <h1>Weather in 5 Major Cities</h1>
        <div id='divPlotly'></div>
        <script>
            var plotly_data = {}
            Plotly.react('divPlotly', plotly_data.data, plotly_data.layout);
        </script>
    </body>
    </html>"""


    # write the JSON to the HTML template
    with open('templates/new_plot.html', 'w') as f:
        f.write(template.format(fig_json))

    return template