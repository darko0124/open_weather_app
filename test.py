import requests
import yaml
import datetime

# Load config from YAML
with open("D:\\Python_Projects\\Github_Repos\\open_weather_app\\config.yaml", "r") as file:  #Change this to be more generic
    config = yaml.safe_load(file)
MAIN_URL = "https://api.openweathermap.org/data/2.5"
api_config = config["openweathermap"]
API_KEY = api_config["api_key"]
CITIES = api_config["cities"]

def get_weather(city):
    WEATHER_URL = f"{MAIN_URL}/weather"

    params = {
        "lat": city["lat"],
        "lon": city["lon"],
        "appid": API_KEY,
        "units": "metric"
    }
    
    response = requests.get(WEATHER_URL, params=params)

    if response.status_code == 200:
        data = response.json()
        location = data.get("name", city["name"])
        print(f"\nThe weather at the moment in {location} is {data['weather'][0]['description']}.\n")
        print(f"Current humidity percentage in {location} is {data['main']['humidity']} %\n")
        print(f"Current temperature in {location} is {data['main']['temp']}°C\n")
    else:
        print(f"Error fetching weather for {city['name']} :",
            response.status_code, response.json())

def get_forecast(city):
    #Url to get current weather (for 3-hourly temperature, because of free api restrictions)
    FORECAST_URL = f"{MAIN_URL}/forecast"
    
    forecast_params = {
        "lat": city["lat"],
        "lon": city["lon"],
        "appid": API_KEY,
        "units": "metric"
    }
        
    forecast_response = requests.get(FORECAST_URL, params = forecast_params)
    
    if forecast_response.status_code == 200:
        forecast_data = forecast_response.json()
        location = forecast_data.get("city", {}).get("name", city["name"])
        print(f"\n3 hour forecast for {location}:\n")
        
        for element in forecast_data.get("list",[])[:8]:
            time_str = element["dt_txt"]
            time_obj = datetime.datetime.strptime(time_str, "%Y-%m-%d %H:%M:%S")
            formatted_time = time_obj.strftime("%H:%M")
            temp = element["main"]["temp"]
            print(f"{formatted_time} -- {temp} °C")
    else:
        print(f"Error fetching weather for {city['name']} :", forecast_response.status_code)

for city in CITIES:
    get_weather(city)
    get_forecast(city)