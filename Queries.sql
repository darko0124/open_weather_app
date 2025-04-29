-- How many distinct weather conditions were observed (rain/snow/clear/...) in a
-- certain period?
select distinct(fw.weather_condition) from forecast_weather fw where date(forecast_time) >='2025-04-29' and date(forecast_time) <= '2025-05-03';

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
join city c on fw.city_id = c.city_id
WHERE
    DATE(fw.forecast_time) BETWEEN '2025-04-29' AND '2025-05-03'
GROUP BY
    fw.city_id, fw.weather_condition
ORDER BY
    fw.city_id, condition_rank
 ) as ranked
 where condition_rank = 1
ORDER BY
    city_id;