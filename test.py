import requests
import yaml
import datetime
import pymysql
import os

# Load config from YAML
with open("D:\\Python_Projects\\Github_Repos\\open_weather_app\\config.yaml", "r") as file:  #Change this to be more generic
    config = yaml.safe_load(file)
MAIN_URL = "https://api.openweathermap.org/data/2.5"
api_config = config["openweathermap"]
API_KEY = api_config["api_key"]
CITIES = api_config["cities"]

def load_config():
    config_path = os.path.join(os.path.dirname(__file__), "config.yaml")  # Automatically resolves path
    with open(config_path, "r") as file:
        return yaml.safe_load(file)
    
# Connect to DB
def connect_to_db(db_config):
    try:
        conn = pymysql.connect(
            database = db_config["dbname"],
            user = db_config["user"],
            password = db_config["password"],
            host = db_config["host"],
            port = db_config["port"]
        )
        cur = conn.cursor()
        if conn.open:
                print("✅ Successfully connected to the database.")
        else:
                print("❌ Failed to open database connection.")
                return None
        
        return conn

    except Exception as e:
        print(f"❌ Error connecting to the database: {e}")
        return None

def get_weather(city, API_KEY):
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

def get_forecast(city, API_KEY):
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
        print("Time -- Temperature -- Humidity -- Weather -- Wind Speed")
        for element in forecast_data.get("list",[])[:8]:
            time_str = element["dt_txt"]
            time_obj = datetime.datetime.strptime(time_str, "%Y-%m-%d %H:%M:%S")
            formatted_time = time_obj.strftime("%H:%M")
            temp = element["main"]["temp"]
            humidity = element["main"]["humidity"]
            weather_condition = element["weather"][0]["main"]
            wind_speed = element["wind"]["speed"]
            print(f"{formatted_time} -- {temp} °C -- {humidity}% -- {weather_condition} -- {wind_speed} m/s")
    else:
        print(f"Error fetching weather for {city['name']} :", forecast_response.status_code)

def main():
    config = load_config()
    api_config = config["openweathermap"]
    API_KEY = api_config["api_key"]
    CITIES = api_config["cities"]

# Optional: Connect to DB if needed
    conn = connect_to_db(config["database"])
    cur = conn.cursor()

    for city in CITIES:
        get_weather(city, API_KEY)
        get_forecast(city, API_KEY)
        
    conn.close()

if __name__ == "__main__":
    main()