import requests
import json
import os
from datetime import datetime
from dotenv import load_dotenv

load_dotenv()

OWM_KEY = os.getenv("OWM_KEY")
DATALAKE = os.getenv("DATALAKE_PATH", "./datalake")
BASE_URL = "http://api.openweathermap.org/data/2.5/onecall/timemachine"

# Coordonnées GPS des stades de Ligue 1
STADIUMS = {
    "Paris Saint-Germain": {"lat": 48.8414, "lon": 2.2530},
    "Olympique de Marseille": {"lat": 43.2696, "lon": 5.3956},
    "Olympique Lyonnais": {"lat": 45.7653, "lon": 4.9822},
    "AS Monaco": {"lat": 43.7272, "lon": 7.4155},
    "LOSC Lille": {"lat": 50.6120, "lon": 3.1304},
    "Stade Rennais": {"lat": 48.1073, "lon": -1.7126},
    "RC Lens": {"lat": 50.4327, "lon": 2.8148},
    "OGC Nice": {"lat": 43.7054, "lon": 7.1927},
}

def save_raw(data, stadium, date_str):
    path = os.path.join(DATALAKE, "raw", "weather", stadium.replace(" ", "_"), date_str)
    os.makedirs(path, exist_ok=True)
    filepath = os.path.join(path, "conditions.json")
    with open(filepath, "w") as f:
        json.dump(data, f, indent=2)
    print(f"✅ Sauvegardé : {filepath}")

def fetch_weather(stadium, lat, lon, date_str):
    print(f"🌤️  Météo pour {stadium} le {date_str}...")
    dt = int(datetime.strptime(date_str, "%Y-%m-%d").timestamp())
    response = requests.get(BASE_URL, params={
        "lat": lat,
        "lon": lon,
        "dt": dt,
        "appid": OWM_KEY,
        "units": "metric"
    })
    data = response.json()
    save_raw(data, stadium, date_str)

if __name__ == "__main__":
    # Dates de matchs à récupérer
    match_dates = ["2024-09-15", "2024-10-06", "2024-11-10"]
    
    for date_str in match_dates:
        for stadium, coords in STADIUMS.items():
            fetch_weather(stadium, coords["lat"], coords["lon"], date_str)
    
    print("✅ Ingestion météo terminée !")