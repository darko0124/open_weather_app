import requests
import yaml

# Load config from YAML
with open("D:\\Python_Projects\\Github_Repos\\open_weather_app\\config.yaml", "r") as file:  #Change this to be more generic
    config = yaml.safe_load(file)

api_config = config["openweathermap"]
API_KEY = api_config["api_key"]
CITIES = api_config["cities"]

BASE_URL = "https://api.openweathermap.org/data/2.5/weather"

for city in CITIES:
    params = {
        "lat": city["lat"],
        "lon": city["lon"],
        "appid": API_KEY,
        "units": "metric"
    }
    
    response = requests.get(BASE_URL, params=params)

    if response.status_code == 200:
        data = response.json()
        location = data.get("name", city["name"])
        print(f"The weather in {location} is {data['weather'][0]['description']}.\n")
        print(f"Humidity percentage in {location} is {data['main']['humidity']} %\n")
        print(f"Current temperature in {location} is {data['main']['temp']}°C\n")
    else:
        print(f"Error fetching weather for {city['name']} :",
            response.status_code, response.json())
