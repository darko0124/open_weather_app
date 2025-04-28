CREATE TABLE city (
    city_id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    latitude DECIMAL(9,6),
    longitude DECIMAL(9,6)
);


CREATE TABLE current_weather (
    id INT AUTO_INCREMENT PRIMARY KEY,
    city_id INT NOT NULL,
    weather_description VARCHAR(255) NOT NULL,
    humidity INT NOT NULL,
    temperature FLOAT NOT NULL,
    timestamp TIMESTAMP default CURRENT_TIMESTAMP,
    pressure INT,
    foreign key (city_id) references city(city_id)
);

CREATE TABLE forecast_weather (
    id INT AUTO_INCREMENT PRIMARY KEY,
    city_id INT NOT NULL,
    forecast_time TIMESTAMP NOT NULL,
    temperature FLOAT NOT NULL,
    humidity INT NOT NULL,
    weather_condition VARCHAR(100) NOT NULL,
    wind_speed FLOAT NOT null,
    foreign key (city_id) references city(city_id)
);