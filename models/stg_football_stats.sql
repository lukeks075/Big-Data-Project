{{ config(materialized='table') }}

WITH raw_football AS (
    SELECT * FROM read_json_auto('datalake/raw/football/players_stats/**/*.json')
),
expanded_teams AS (
    SELECT UNNEST(response) AS team_data
    FROM raw_football
),
expanded_players AS (
    SELECT 
        team_data['team']['name']::VARCHAR AS club,
        UNNEST(team_data['players']) AS player_data
    FROM expanded_teams
)
SELECT
    player_data['player']['id']::INTEGER AS player_id,
    player_data['player']['name']::VARCHAR AS player_name,
    club,
    player_data['statistics'][1]['games']['minutes']::INTEGER AS minutes_played,
    1 AS matches_played,
    player_data['statistics'][1]['games']['position']::VARCHAR AS position,
    player_data['statistics'][1]['games']['rating']::FLOAT AS rating,
    CURRENT_DATE AS match_date
FROM expanded_players
WHERE player_data['statistics'][1]['games']['minutes'] IS NOT NULL