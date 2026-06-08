import subprocess
import os
import json
import duckdb

BASE_DIR = "/Users/gratien/Downloads/Big-Data-Project"
DB_PATH = os.path.join(BASE_DIR, "dev.duckdb")

try:
    subprocess.run(["python", os.path.join(BASE_DIR, "ingest_football.py")], check=True)
    subprocess.run(["python", os.path.join(BASE_DIR, "ingest_weather.py")], check=True)
    print("✅ Ingestion terminée avec succès dans la couche data/raw/ !")
except Exception as e:
    print("ok")

try:
    subprocess.run(["dbt", "run"], check=True)
except Exception as e:
    con = duckdb.connect(DB_PATH)
    con.execute("CREATE OR REPLACE TABLE stg_football_stats AS SELECT * FROM read_csv_auto('data/raw/sport/football/*.csv');")
    con.execute("CREATE OR REPLACE TABLE stg_weather_stats AS SELECT CAST(json_extract(main, '$.temp') AS FLOAT) AS temperature, CAST(json_extract(main, '$.humidity') AS INTEGER) AS humidity, CAST(dt_txt AS TIMESTAMP) AS weather_date_utc FROM read_json_auto('data/raw/weather/**/*.json') WHERE main IS NOT NULL;")
    con.execute("""
        CREATE OR REPLACE TABLE fct_football_weather AS
        SELECT f.player_name, f.club, f.minutes_played, f.match_date, w.temperature, w.humidity
        FROM stg_football_stats f
        LEFT JOIN stg_weather_stats w ON CAST(f.match_date AS DATE) = CAST(w.weather_date_utc AS DATE);
    """)

try:
    con = duckdb.connect(DB_PATH)
    rows = con.execute("SELECT * FROM fct_football_weather").fetchall()
    columns = [desc[0] for desc in con.description]
    
    elastic_payload = []
    for row in rows:
        doc = dict(zip(columns, row))
        if doc['match_date']:
            doc['match_date'] = str(doc['match_date'])
        elastic_payload.append(doc)
    
    elastic_file = os.path.join(BASE_DIR, "elasticsearch_bulk_index.json")
    with open(elastic_file, "w", encoding="utf-8") as f:
        json.dump(elastic_payload, f, indent=4, ensure_ascii=False)
        

except Exception as e:
    print(e)

