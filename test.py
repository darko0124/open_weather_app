import requests
import yaml
import datetime
import pymysql
import os
import pandas as pd

# # Load config from YAML
# with open("D:\\Python_Projects\\Github_Repos\\open_weather_app\\config.yaml", "r") as file:  #Change this to be more generic
#     config = yaml.safe_load(file)

# api_config = config["openweathermap"]
# API_KEY = api_config["api_key"]
# CITIES = api_config["cities"]

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

def get_weather(city, API_KEY, MAIN_URL):
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
            "city_id": city["id"],  # <<<<< VERY IMPORTANT!
            "temperature": data["main"]["temp"],
            "humidity": data["main"]["humidity"],
            "pressure": data["main"]["pressure"],
            "weather_description": data["weather"][0]["description"],
        }
        
    else:
        print(f"Error fetching weather for {city['name']} :",
        response.status_code, response.json())

# def get_forecast(city, API_KEY, MAIN_URL):
#     FORECAST_URL = f"{MAIN_URL}/forecast"
    
#     forecast_params = {
#         "lat": city["lat"],
#         "lon": city["lon"],
#         "appid": API_KEY,
#         "units": "metric"
#     }
        
#     forecast_response = requests.get(FORECAST_URL, params=forecast_params)
    
#     if forecast_response.status_code == 200:
#         forecast_data = forecast_response.json()
#         location = forecast_data.get("city", {}).get("name", city["name"])

#         forecast_list = []
#         for element in forecast_data.get("list", [])[:8]:  # Next 24 hours (8 x 3h = 24h)
#             time_str = element["dt_txt"]
#             temp = element["main"]["temp"]
#             humidity = element["main"]["humidity"]
#             weather_condition = element["weather"][0]["main"]
#             wind_speed = element["wind"]["speed"]

#             forecast_list.append({
#                 "city": location,
#                 "forecast_time": time_str,
#                 "temperature": temp,
#                 "humidity": humidity,
#                 "weather_condition": weather_condition,
#                 "wind_speed": wind_speed
#             })
#         return forecast_list
#     else:
#         print(f"Error fetching forecast for {city['name']} :", forecast_response.status_code)
#         return []
    
def insert_data(cur, table_name, data, columns):
    """
    Generic function to insert data into any table.

    :param cur: The cursor object used to interact with the database.
    :param table_name: The name of the table where data will be inserted.
    :param data: A list of dictionaries where each dictionary represents a row to be inserted.
    :param columns: A list of column names in the same order as the data to be inserted.
    """
    # Construct the placeholders for SQL query (%s for each column)
    placeholders = ', '.join(['%s'] * len(columns))
    insert_query = f"INSERT INTO {table_name} ({', '.join(columns)}) VALUES ({placeholders})"
    print(insert_query)
    
    for row in data:
        try:
            # Extract values from the row dictionary in the same order as the columns
            values = [row[column] for column in columns]
            print(values)

            cur.execute(insert_query, values)
            
            # Check if a row was affected
            if cur.rowcount > 0:
                print(f"✅ Data for {row['city_id']} inserted successfully.")
            else:
                print(f"❌ No rows inserted for {row['city_id']}.")
        except Exception as e:
            print(f"❌ Error inserting data for {row['city_id']}: {e}")

def insert_weather_data(cur, weather_data):
    columns = ["city_id", "weather_description", "humidity", "temperature", "pressure"]
    insert_data(cur, "current_weather", [weather_data], columns)


def select_data(cur, query, params=None):
    """
    Executes a SELECT query and returns the result.

    :param cur: The cursor object used to interact with the database.
    :param query: The SQL SELECT query to be executed.
    :param params: Optional tuple/list of parameters for parameterized query execution.
    :return: Result of the query (list of tuples).
    """
    try:
        # If parameters are provided, use them in the query
        if params:
            cur.execute(query, params)
        else:
            cur.execute(query)

        # Fetch all rows from the query result
        result = cur.fetchall()

        if result:
            print("✅ Data fetched successfully.")
        else:
            print("❌ No data found for the query.")

        return result
    except Exception as e:
        print(f"❌ Error executing query: {e}")
        return None
    
def get_cities_data(cur, query):
    result = select_data(cur, query)
    cities_df = pd.DataFrame(result, columns=["id", "name", "lat", "lon"])
    return cities_df
    
def main():
    config = load_config()
    api_config = config["openweathermap"]
    database_config = config["database"]
    queries_config = config["queries"]
    API_KEY = api_config["api_key"]
    MAIN_URL = "https://api.openweathermap.org/data/2.5"
    
    conn = connect_to_db(config["database"])
    cur = conn.cursor()
     # Get cities from DB
    cities_df = get_cities_data(cur, queries_config["get_city_names"])

    # Loop through each city
    for index, city in cities_df.iterrows():
        weather_data = get_weather(city, API_KEY, MAIN_URL)
        if weather_data:
            insert_weather_data(cur, weather_data)

    # Commit and close
    conn.commit()
    conn.close()
    print("✅ All done!")
    
if __name__ == "__main__":
    main()