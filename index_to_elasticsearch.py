import duckdb
import json
import requests
import os
from dotenv import load_dotenv

load_dotenv()

ES_HOST = os.getenv("ES_HOST", "http://localhost:9200")
ES_INDEX = os.getenv("ES_INDEX", "injury_risk")
DB_PATH = "datalake/duckdb_project.db"

print("📡 Connexion à DuckDB...")
con = duckdb.connect(DB_PATH)

print("📊 Récupération des données combinées...")
rows = con.execute("SELECT * FROM fct_football_weather").fetchall()
columns = [desc[0] for desc in con.description]
print(f"✅ {len(rows)} documents à indexer")

print("🔍 Création de l'index Elasticsearch...")
requests.delete(f"{ES_HOST}/{ES_INDEX}")
requests.put(f"{ES_HOST}/{ES_INDEX}", json={
    "mappings": {
        "properties": {
            "player_id": {"type": "integer"},
            "player_name": {"type": "keyword"},
            "club": {"type": "keyword"},
            "minutes_played": {"type": "integer"},
            "match_date": {"type": "date"},
            "temperature": {"type": "float"},
            "humidity": {"type": "integer"},
            "cloudiness": {"type": "integer"},
        }
    }
})

print("📤 Indexation des documents...")
for row in rows:
    doc = dict(zip(columns, row))
    if doc.get("match_date"):
        doc["match_date"] = str(doc["match_date"])
    requests.post(f"{ES_HOST}/{ES_INDEX}/_doc", json=doc)

print(f"✅ {len(rows)} documents indexés dans '{ES_INDEX}' !")
print(f"🌐 Ouvre Kibana sur http://localhost:5601")