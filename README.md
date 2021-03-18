### Cloudy With a Chance of Snakes: A Python Weather App
#### Introduction
A Pthon Weather App is an web-based app that allows to users to get weather data based on their location, such as cities. Users can also compare daily weather forecast in term of minimum temperature, maximum temperature, feels like, humidity, and pressure among cities by dynamically adding or removing cities.

Main technologies: Python Flask (backend); HTML, CSS, and JavaScript (front-end)
#### How to Run 
* * * 
1. Clone the Repo to local directory of your choice
    - command: ```$ git clone https://github.com/gtshepard/cloudy-with-a-chance-of-snakes.git```
* * * 
2. create a python virtual environment for this project (make sure it is in a seperate directory from the actual project code)
   - command: ```$ python3 -m venv /your-environment-dir```. For example, '''$ python3 -m venv venv'''
* * * 
3. startup virtual environment 

    - command:  ```$ cd /your-environment-dir```

    - command: ```$ source bin/activate ```
* * * 
4. navigate to project directory and install dependencies

     - command:  ```$ pip3 install -r requirements.txt```
* * *   
5. set environment variables 
    - command: ```export FLASK_APP=app.py```
* * * 
6. run app from local directory 
    - command: ```flask run```
* * * 
