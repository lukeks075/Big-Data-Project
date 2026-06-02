{{ config(materialized='table') }}

WITH raw_weather AS (
    SELECT * FROM read_json_auto('datalake/raw/weather/**/*.json')
)
SELECT
    CAST(main->>'temp' AS FLOAT) AS temperature,
    CAST(main->>'humidity' AS INTEGER) AS humidity,
    CAST(clouds->>'all' AS INTEGER) AS cloudiness,
    CAST(dt_txt AS TIMESTAMP) AS weather_date
FROM raw_weather