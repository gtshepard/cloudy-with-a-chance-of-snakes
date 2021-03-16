### Cloudy With a Chance of Snakes: A Python Weather App


#### How to Run 


1. Clone the Repo to local directory of your choice
  ```$ git clone repo```
2. create a python virtual environment for this project (make sure it is in a seperate directory from the actual project code)
   ```$ python3 -m venv /some_path/your-environment-dir```
   
3. startup virtual environment 

  ```$ cd /your-environment-dir```
  ```$ source bin/activate ```
   
4. navigate to project directory and install dependencies

   ```$ pip3 install -r requirenments.txt```

4. get copy of ```env``` from slack and rename to ```.env```

   ```$ mv env .env ```
  
5. set environment variables 
   ```export FLASK_APP=app.py```

6. run app from local directory 
   ```flask run```
