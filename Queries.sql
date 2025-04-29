-- How many distinct weather conditions were observed (rain/snow/clear/...) in a
-- certain period?
SELECT DISTINCT(fw.weather_condition)
FROM forecast_weather fw
WHERE DATE(fw.forecast_time) >= '2025-04-29'
AND DATE(fw.forecast_time) <= '2025-05-03';

-- Rank the most common weather conditions in a certain period of time per city?
SELECT
    city_id,
    name,
    weather_condition,
    condition_count,
    condition_rank
FROM (
SELECT
    fw.city_id,
    c.name,
    fw.weather_condition,
    COUNT(fw.weather_condition) AS condition_count,
    RANK() OVER (PARTITION BY fw.city_id ORDER BY COUNT(*) DESC) AS condition_rank
FROM
    forecast_weather fw
JOIN city c ON fw.city_id = c.city_id
WHERE
    DATE(fw.forecast_time) BETWEEN '2025-04-29' AND '2025-05-03'
GROUP BY
    fw.city_id, fw.weather_condition
ORDER BY
    fw.city_id, condition_rank
 ) AS ranked
 WHERE condition_rank = 1
ORDER BY
    city_id;

-- What are the temperature averages observed in a certain period per city?
SELECT DISTINCT(c.name), round(avg(fw.temperature),2) AS temperature_average
FROM forecast_weather fw
JOIN city c ON fw.city_id = c.city_id
WHERE
    DATE(fw.forecast_time) BETWEEN '2025-01-29' AND '2025-05-03'
GROUP BY
    fw.city_id, c.name
ORDER BY c.name

-- What city had the highest absolute temperature in a certain period of time?
SELECT
    c.name AS city_name,
    MAX(fw.temperature) AS highest_temperature
FROM
    forecast_weather fw
JOIN
    city c ON fw.city_id = c.city_id
WHERE
    DATE(fw.forecast_time) BETWEEN '2025-04-29' AND '2025-05-03' 
GROUP BY
    c.name
ORDER BY
    highest_temperature DESC
LIMIT 1;

-- Which city had the highest daily temperature variation in a certain period of time?
SELECT
    c.name AS city_name,
    ROUND(MAX(fw.temperature) - MIN(fw.temperature), 2) AS daily_temperature_variation
FROM
    forecast_weather fw
JOIN
    city c ON fw.city_id = c.city_id
WHERE
    DATE(fw.forecast_time) BETWEEN '2025-04-29' AND '2025-05-03'
GROUP BY
    c.name
ORDER BY
    daily_temperature_variation DESC
LIMIT 1;

-- Which city had the strongest wind in a certain period of time ?
select 
	c.name as city_name,
	MAX(fw.wind_speed) as max_wind_speed
from
	forecast_weather fw 
join city c on fw.city_id  = c.city_id 
where 
	DATE(fw.forecast_time) BETWEEN '2025-04-29' AND '2025-05-03'
GROUP BY
    c.name
ORDER by max_wind_speed desc
limit 1;