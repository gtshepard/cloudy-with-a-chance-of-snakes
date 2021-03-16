from flask import Flask,render_template
import requests 
import plotly.graph_objects
from os import environ, path
from dotenv import load_dotenv

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
    for item in response['list']:
        #t_min, t_max, date = response['list'][1]['main']['temp_min'],response['list'][1]['main']['temp_max'], response['list'][1]['dt_txt']
        t_min = item['main']['temp_min']
        date = item['dt_txt']
        t_mins.append(float(t_min))
        dates.append(date)
        

    make_plot_2(t_mins, dates)
    return render_template('new_plot.html')

@app.route("/data")
def see_data():
    response = get_weather_by_location('42.54149775840134','-75.01959026744706' )
    #print(response['list'][0][''])
    return response['list'][1]



def get_weather_by_location(lat, lon):
    location_search = f'weather?lat={lat}&lon={lon}&appid={API_KEY}'
    location_search_weeks = f'forecast?&units=imperial&lat={lat}&lon={lon}&appid={API_KEY}'

    response = requests.get(BASE_URL + location_search_weeks)
    return response.json()


def make_plot_2(t_mins, dates):
    # create a simple plot

    line = plotly.graph_objs.Scatter(x=dates, 
                                y=t_mins)
    layout = plotly.graph_objs.Layout()
    fig = plotly.graph_objs.Figure([line], layout)

    # convert it to JSON
    fig_json = fig.to_json()

    # a simple HTML template
    template = """<html>
    <head>
        <script src="https://cdn.plot.ly/plotly-latest.min.js"></script>
    </head>
    
    <body>
        <h1>cookies and cream</h1>
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