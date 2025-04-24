import requests
import yaml

with open("D:\Python_Projects\Github_Repos\open_weather_app\config.yaml", "r") as file:  #Change this to be more generic
    config = yaml.safe_load(file)
    
API_KEY = config["openweathermap"]["api_key"]
CITY_NAME = "London"
BASE_URL = "https://api.openweathermap.org/data/2.5/weather"

params = {
    "q": CITY_NAME,
    "appid": API_KEY,
    "units": "metric"
}

response = requests.get(BASE_URL, params=params)

if response.status_code == 200:
    data = response.json()
    print(f"Weather in {CITY_NAME}: {data['weather'][0]['description']}")
    print(f"Temperature: {data['main']['temp']}°C")
else:
    print("Error:", response.status_code, response.json())