{{ config(materialized='table') }}

WITH football AS (
    -- On appelle la table de foot nettoyée
    SELECT * FROM {{ ref('stg_football_stats') }}
),

weather AS (
    -- On appelle la table météo nettoyée
    SELECT * FROM {{ ref('stg_weather_stats') }}
)

SELECT
    f.player_id,
    f.player_name,
    f.minutes_played,
    f.matches_played,
    f.match_date,
    w.temperature,
    w.humidity,
    w.cloudiness
FROM football f
-- Jointure sur la date du match
LEFT JOIN weather w 
    ON CAST(f.match_date AS DATE) = CAST(w.weather_date AS DATE)