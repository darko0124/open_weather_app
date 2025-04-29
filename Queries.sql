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
    DATE(fw.forecast_time) BETWEEN '2025-01-29' AND '2025-05-03' #This can be changed to user input
GROUP BY
    fw.city_id, c.name
ORDER BY c.name