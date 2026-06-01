import requests
import json
import os
from datetime import datetime
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("API_SPORTS_KEY")
BASE_URL = "https://v3.football.api-sports.io"
LEAGUE_ID = int(os.getenv("LEAGUE_ID", 61))
SEASON = int(os.getenv("SEASON", 2024))
DATALAKE = os.getenv("DATALAKE_PATH", "./datalake")

headers = {"x-apisports-key": API_KEY}

def save_raw(data, folder, filename):
    today = datetime.utcnow().strftime("%Y-%m-%d")
    path = os.path.join(DATALAKE, "raw", folder, today)
    os.makedirs(path, exist_ok=True)
    filepath = os.path.join(path, filename)
    with open(filepath, "w") as f:
        json.dump(data, f, indent=2)
    print(f"✅ Sauvegardé : {filepath}")

def fetch_fixtures():
    print("📡 Récupération des matchs Ligue 1...")
    response = requests.get(
        f"{BASE_URL}/fixtures",
        headers=headers,
        params={"league": LEAGUE_ID, "season": 2024, "from": "2024-08-01", "to": "2024-12-31"}
    )
    data = response.json()
    save_raw(data, "football/fixtures", "fixtures.json")
    return data

def fetch_players_stats(fixture_id):
    print(f"📡 Récupération stats joueurs pour match {fixture_id}...")
    response = requests.get(
        f"{BASE_URL}/fixtures/players",
        headers=headers,
        params={"fixture": fixture_id}
    )
    data = response.json()
    save_raw(data, "football/players_stats", f"players_{fixture_id}.json")

if __name__ == "__main__":
    fixtures = fetch_fixtures()
    fixture_ids = [f["fixture"]["id"] for f in fixtures.get("response", [])]
    print(f"🏟️  {len(fixture_ids)} matchs trouvés")
    for fid in fixture_ids[:3]:  # on prend les 3 premiers pour tester
        fetch_players_stats(fid)
    print("✅ Ingestion football terminée !")