import requests
import yaml

# Load config from YAML
with open("D:\\Python_Projects\\Github_Repos\\open_weather_app\\config.yaml", "r") as file:  #Change this to be more generic
    config = yaml.safe_load(file)

api_config = config["openweathermap"]
API_KEY = api_config["api_key"]
LAT = api_config["lat"]
LON = api_config["lon"]

BASE_URL = "https://api.openweathermap.org/data/2.5/weather"

params = {
    "lat": LAT,
    "lon": LON,
    "appid": API_KEY,
    "units": "metric"
}

response = requests.get(BASE_URL, params=params)

if response.status_code == 200:
    data = response.json()
    location = data.get("name", "Unknown Location")
    print(f"Weather in {location}: {data['weather'][0]['description']}")
    print(f"Temperature: {data['main']['temp']}°C")
else:
    print("Error:", response.status_code, response.json())
