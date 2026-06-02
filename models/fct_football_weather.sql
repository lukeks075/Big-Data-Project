{{ config(materialized='table') }}

WITH football AS (
    SELECT * FROM {{ ref('stg_football_stats') }}
),
weather AS (
    SELECT * FROM {{ ref('stg_weather_stats') }}
)
SELECT
    f.player_id,
    f.player_name,
    f.club,
    f.minutes_played,
    f.matches_played,
    f.position,
    f.rating,
    f.match_date,
    w.temperature,
    w.humidity,
    w.cloudiness,
    w.weather_date
FROM football f
LEFT JOIN weather w ON CAST(f.match_date AS DATE) = CAST(w.weather_date AS DATE)