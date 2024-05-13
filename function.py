from dotenv import load_dotenv #pip install python-dotenv
import requests #pip install requests
import os
import dataBaseConnect
import datetime
from flask import request,session
from werkzeug.security import generate_password_hash, check_password_hash


load_dotenv()
API_KEY=os.getenv('API_KEY')


def session_check():
    if 'username' not in session:
        return "NO"
    return session['username']

def checkPremuim():
    value=dataBaseConnect.get_premuim(session['username'])
    return value

def getOneWeatherDetails(city):
    url = 'http://api.openweathermap.org/data/2.5/forecast?q={}&units=imperial&appid='+ API_KEY
    
    r = requests.get(url.format(city)).json()
    forecast_data = []
    
    if 'list' in r:
        for data in r['list'][:6]:  
            forecast = {
                'city': city,
                'date_time': datetime.datetime.fromtimestamp(data['dt']).strftime("%d %b %Y | %I:%M:%S %p"),
                'temperature': int((data['main']['temp'] - 32) * 5/9),
                'description': data['weather'][0]['description'],
                'icon': data['weather'][0]['icon'],
                'humidity': data['main']['humidity'],
                'pressure': data['main']['pressure'],
                'wind_speed': data['wind']['speed'],
                'min_temperature': int((data['main']['temp_min'] - 32) * 5/9),
                'max_temperature': int((data['main']['temp_max'] - 32) * 5/9),
                # Add more forecast variables as needed
            }
            forecast_data.append(forecast)
    
    return forecast_data





    # url = 'http://api.openweathermap.org/data/2.5/weather?q={}&units=imperial&appid=271d1234d3f497eed5b1d80a07b3fcd1'
    
    # r = requests.get(url.format(city)).json()
    # weather_data = []
    
    # if 'main' in r and 'weather' in r:
    #     weather = {
    #         'city': city,
    #         'temperature':  int((r['main']['temp'] - 32) * 5/9),
    #         'description': r['weather'][0]['description'],
    #         'icon': r['weather'][0]['icon'],
    #         'date_time': datetime.datetime.now().strftime("%d %b %Y | %I:%M:%S %p"),
    #         'humidity': r['main']['humidity'],
    #         'pressure': r['main']['pressure'],
    #         'wind_speed': r['wind']['speed'],
    #         'visibility': r['visibility'] / 1000,
    #         'sunrise': datetime.datetime.fromtimestamp(r['sys']['sunrise']).strftime("%H:%M:%S"),
    #         'sunset': datetime.datetime.fromtimestamp(r['sys']['sunset']).strftime("%H:%M:%S"),
    #         'cloudiness': r['clouds']['all'],
    #         'feels_like': int((r['main']['feels_like'] - 32) * 5/9),
    #         'min_temperature': int((r['main']['temp_min'] - 32) * 5/9),
    #         'max_temperature': int((r['main']['temp_max'] - 32) * 5/9),
    #     }
    #     weather_data.append(weather)
    
    # return weather_data



def getWeather():    
    username = session['username']
    cities = dataBaseConnect.getData(username)
    url = 'http://api.openweathermap.org/data/2.5/weather?q={}&units=imperial&appid=' + API_KEY
    weather_data = [] 
    for city in cities:  
        r = requests.get(url.format(city)).json()
        if 'main' in r and 'weather' in r:
            temperature = int((r['main']['temp'] - 32) * 5/9)
            description = r['weather'][0]['description']
            icon = r['weather'][0]['icon']
            humidity = r['main']['humidity']
            date_time = datetime.datetime.now().strftime("%d %b %Y | %I:%M:%S %p")
            weather = {
                'city': city,
                'temperature': temperature,
                'description': description,
                'icon': icon,
                'date_time': date_time,
                'humidity': humidity,
            }
            weather_data.append(weather)
        else:
            # Handle the case where the required keys are missing in the API response
            print(f"Error: Required keys not found in API response for city: {city}")
    return weather_data


def register_func():
    username = request.form['username']
    email = request.form['email']
    password = request.form['password']
    confirm_password = request.form['confirm_password']
    users=dataBaseConnect.getUsers()
    if email in users:
        return False
    if password != confirm_password:
        return 'not match'
    hashed_password = generate_password_hash(password)
    dataBaseConnect.register_user(username,email,hashed_password)
    session['username'] = username
    

    return True


def login_user():
    username = request.form['username']
    password = request.form['password']
    users=dataBaseConnect.getUserName()
    if username not in users:
        return "not"
    
    encrypt_password=dataBaseConnect.getPassword(username)
    if check_password_hash(encrypt_password, password):
        session['username'] = username
        return True
    # Passwords match, allow login
        return False
    # Passwords don't match, deny login

def logout():
    session.clear()
    
def ins_cities(ispremium):
    cities=dataBaseConnect.getData(session['username'])    
    current_user=session['username']
    new_city = request.form.get('city')
    if new_city:
        if not ispremium:
           
            if new_city.upper() not in [city.upper() for city in cities]:   
                
                if dataBaseConnect.check_record_count(current_user):
            
                    if checkCity(new_city):
                        
                        dataBaseConnect.insert_city(current_user,new_city)
                        return True
                    return "False" 
                return False
            return " City Already Exist"
            
        if new_city not in cities:
            dataBaseConnect.insert_city(current_user,new_city)
            return True

def checkCity(city):
    url = 'http://api.openweathermap.org/data/2.5/weather?q={}&units=imperial&appid='+ API_KEY
    r = requests.get(url.format(city)).json()
    if 'cod' in r and r['cod'] == '404':
        return False
    return True

    