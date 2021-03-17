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
    response = get_weather_by_location('42.54149775840134','-75.01959026744706' )
    t_mins = []
    dates = []
    t_maxs = []
    for item in response['list']:
        #t_min, t_max, date = response['list'][1]['main']['temp_min'],response['list'][1]['main']['temp_max'], response['list'][1]['dt_txt']
        t_min = item['main']['temp_min']
        date = item['dt_txt']
        t_max = item['main']['temp_max']
        t_mins.append(float(t_min))
        dates.append(date)
        t_maxs.append(float(t_max))
        
    make_plot_3()
    #make_plot_2(t_mins,t_maxs, dates)
    return render_template('new_plot.html')

@app.route("/data")
def see_data():
    #response = get_weather_by_location('42.54149775840134','-75.01959026744706' )
    #print(response['list'][0][''])
    response = get_weather_for_city('los angeles')
    return response



def get_weather_by_location(lat, lon):
    location_search = f'weather?lat={lat}&lon={lon}&appid={API_KEY}'
    location_search_weeks = f'forecast?&units=imperial&lat={lat}&lon={lon}&appid={API_KEY}'

    response = requests.get(BASE_URL + location_search_weeks)
    return response.json()

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


def make_plot_3():
    cities = ['new york', 'london','miami', 'dubai', 'los angeles']
    data = get_weather_for_cities(cities)
    city_to_temp = defaultdict(list)
    city_to_humidity = defaultdict(list)
    city_to_feels = defaultdict(list)

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


    for city in cities:
        fig.add_trace(go.Scatter(x=[i for i in range(120)], y=city_to_temp[city], mode='lines', name=f'{city}-t'))

    for city in cities:
        fig.add_trace(go.Scatter(x=[i for i in range(120)], y=city_to_humidity[city], mode='lines', name=f'{city}-h', visible=False))
    
    for city in cities:
        fig.add_trace(go.Scatter(x=[i for i in range(120)], y=city_to_feels[city], mode='lines', name=f'{city}-f', visible=False))


    fig.update_layout(
    updatemenus=[go.layout.Updatemenu(
        active=0,
        buttons=list(
            [dict(method='update', label='Max Temp', args = [{'visible': [True, True, True, True, True, False, False, False, False, False, False, False, False, False, False] },
                          {'title': 'Max Temp',
                           'showlegend':True}]),
            dict(method='update', label='Feels Like', args = [{'visible': [False, False, False, False, False,False, False, False, False, False, True, True, True, True, True]},
                          {'title': 'Feels Like',
                           'showlegend':True}]), 
            dict(method='update', label='Humidity', args = [{'visible': [False, False, False, False, False, True, True, True, True, True, False, False, False, False, False]},
                          {'title': 'Humidity',
                           'showlegend':True, 
                           'yaxis':{'title':'Percentage', 
                           'visible': True, 
                           'showticklabels': True}
                           }]), 
          
            ]),
        )
    ])
    
  
 
    '''
    buttons.append(dict(method='update', label='Max Temp', args = [{'visible': [True, True, True, True, True, False, False, False, False, False]},
                          {'title': 'Max Temp',
                           'showlegend':True}]))
    
    buttons.append(dict(method='update', label='Humidity', args = [{'visible': [False, False, False, False, False, True, True, True, True, True]},
                          {'title': 'Humidity',
                           'showlegend':True}]))
  
    '''
    '''
    buttons.append(dict(method='restyle', label='Feels Like', args=[{'y': city_to_feels[cities[0]],
                               'x':[i for i in range(40)],
                               'type':'scatter'}, [0]],))
    
    '''
    '''
    for item in ('Max Temp', 'Humidity', 'Feels Like'):
        entry = dict(method='restyle', label=item, args=[{'y':[666,777,999],
                               'x':[1,2, 3],
                               'type':'scatter'}, [0]],
                        )
        buttons.append(entry)
    '''
    
    '''
    update_menu = []
    menu = dict()
    update_menu.append(menu)
    update_menu[0]['buttons'] = buttons
    update_menu[0]['direction'] = 'down'
    update_menu[0]['showactive'] = True
    update_menu[0]['active'] = 0

    fig.update_layout(showlegend=True, updatemenus=update_menu)
    '''
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

'''
def make_plot_2(t_mins,t_maxs, dates):
    # create a simple plot
    fig = go.Figure()
    #make_plot_3()
    fig.add_trace(go.Scatter(x=dates, y=t_mins, mode='lines', name='temp mins'))
    fig.add_trace(go.Scatter(x=dates, y=t_maxs, mode='lines', name='temp maxes'))

    
                                
    #layout = go.Layout()
    #fig = plotly.graph_objs.Figure([line], layout)

    # convert it to JSON
    fig_json = fig.to_json()

    # a simple HTML template
    template = """<html>
    <head>
        <script src="https://cdn.plot.ly/plotly-latest.min.js"></script>
    </head>
    
    <body>
        <h1>Weather in 5 major Cities</h1>
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
    
# '42.54149775840134', '-75.01959026744706'
# get base city 
# what kind of data to filter 
# what kind of data to not filter 
# by city? based on city a new set of data is pulled and plot changes 
# top 5 cities and location 
# filter 
# 
'''