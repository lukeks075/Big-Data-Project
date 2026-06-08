import json
import os
import random
from datetime import datetime

DATALAKE = "./datalake"

STADIUMS = [
    "Paris_Saint-Germain", "Olympique_de_Marseille", "Olympique_Lyonnais",
    "AS_Monaco", "LOSC_Lille", "Stade_Rennais", "RC_Lens", "OGC_Nice"
]

MATCH_DATES = ["2024-09-15", "2024-10-06", "2024-11-10"]

def generate_mock_weather(stadium, date_str):
    temp = round(random.uniform(10.0, 20.0), 1)
    humidity = random.randint(60, 95)  
    clouds = random.randint(10, 100)  
    
    weather_data = {
        "main": {
            "temp": temp,
            "humidity": humidity,
            "feels_like": round(temp - 1.2, 1),
            "temp_min": round(temp - 3.0, 1),
            "temp_max": round(temp + 2.0, 1)
        },
        "clouds": {
            "all": clouds
        },
        "dt_txt": f"{date_str} 20:45:00", 
        "cod": 200
    }
    
    path = os.path.join(DATALAKE, "raw", "weather", stadium, date_str)
    os.makedirs(path, exist_ok=True)
    
    filepath = os.path.join(path, "conditions.json")
    with open(filepath, "w", encoding="utf-8") as f:
        json.dump(weather_data, f, indent=2)
    print(f" Mock météo généré pour {stadium} ({date_str}) -> {temp}°C, {humidity}% Humidité")

if __name__ == "__main__":
    print(" Nettoyage des anciens fichiers d'erreur...")
    import shutil
    weather_dir = os.path.join(DATALAKE, "raw", "weather")
    if os.path.exists(weather_dir):
        shutil.rmtree(weather_dir)
        
    print(" Début de la génération des données météo gratuites...")
    for date in MATCH_DATES:
        for stadium in STADIUMS:
            generate_mock_weather(stadium, date)
            
    print("\n Ingestion météo simulée terminée avec succès (100% Gratuit) !")