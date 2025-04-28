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
        weather_description = data['weather'][0]['description']
        humidity = data['main']['humidity']
        temperature = data['main']['temp']
        
        return {
            "city": location,
            "weather_description": weather_description,
            "humidity": humidity,
            "temperature": temperature,
            "timestamp": datetime.datetime.now(datetime.UTC)
        }
        
    else:
        print(f"Error fetching weather for {city['name']} :",
            response.status_code, response.json())

def get_forecast(city, API_KEY):
    FORECAST_URL = f"{MAIN_URL}/forecast"
    
    forecast_params = {
        "lat": city["lat"],
        "lon": city["lon"],
        "appid": API_KEY,
        "units": "metric"
    }
        
    forecast_response = requests.get(FORECAST_URL, params=forecast_params)
    
    if forecast_response.status_code == 200:
        forecast_data = forecast_response.json()
        location = forecast_data.get("city", {}).get("name", city["name"])

        forecast_list = []
        for element in forecast_data.get("list", [])[:8]:  # Next 24 hours (8 x 3h = 24h)
            time_str = element["dt_txt"]
            temp = element["main"]["temp"]
            humidity = element["main"]["humidity"]
            weather_condition = element["weather"][0]["main"]
            wind_speed = element["wind"]["speed"]

            forecast_list.append({
                "city": location,
                "forecast_time": time_str,
                "temperature": temp,
                "humidity": humidity,
                "weather_condition": weather_condition,
                "wind_speed": wind_speed
            })
        return forecast_list
    else:
        print(f"Error fetching forecast for {city['name']} :", forecast_response.status_code)
        return []

def insert_weather_data(cur, weather_data):
    insert_query = """
    INSERT INTO current_weather (city, weather_description, humidity, temperature, timestamp)
    VALUES (%s, %s, %s, %s, %s)
    """
    try:
        cur.execute(insert_query, (
            weather_data["city"],
            weather_data["weather_description"],
            weather_data["humidity"],
            weather_data["temperature"],
            weather_data["timestamp"]
        ))
        
        # Check if a row was affected
        if cur.rowcount > 0:
            print(f"✅ Weather data for {weather_data['city']} inserted successfully.")
        else:
            print(f"❌ No rows inserted for {weather_data['city']}.")
        
    except Exception as e:
        print(f"❌ Error inserting weather data for {weather_data['city']}: {e}")

def insert_forecast_data(cur, forecast_data_list):
    insert_query = """
    INSERT INTO forecast_weather (city, forecast_time, temperature, humidity, weather_condition, wind_speed)
    VALUES (%s, %s, %s, %s, %s, %s)
    """
    for forecast_data in forecast_data_list:
        try:
            cur.execute(insert_query, (
                forecast_data["city"],
                forecast_data["forecast_time"],
                forecast_data["temperature"],
                forecast_data["humidity"],
                forecast_data["weather_condition"],
                forecast_data["wind_speed"]
            ))
            
            # Check if a row was affected
            if cur.rowcount > 0:
                print(f"✅ Forecast data for {forecast_data['city']} at {forecast_data['forecast_time']} inserted successfully.")
            else:
                print(f"❌ No rows inserted for {forecast_data['city']} at {forecast_data['forecast_time']}.")
                
        except Exception as e:
            print(f"❌ Error inserting forecast data for {forecast_data['city']} at {forecast_data['forecast_time']}: {e}")
        
def main():
    config = load_config()
    api_config = config["openweathermap"]
    API_KEY = api_config["api_key"]
    CITIES = api_config["cities"]

# Optional: Connect to DB if needed
    conn = connect_to_db(config["database"])
    cur = conn.cursor()

    for city in CITIES:
        weather_data = get_weather(city, API_KEY)
        if weather_data:
            insert_weather_data(cur, weather_data)

        forecast_data_list = get_forecast(city, API_KEY)
        if forecast_data_list:
            insert_forecast_data(cur, forecast_data_list)
    
    conn.commit()
    conn.close()

if __name__ == "__main__":
    main()