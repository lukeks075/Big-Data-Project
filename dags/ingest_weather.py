import os
import pandas as pd
from datetime import datetime

print("Démarrage de l'ingestion des données Météo...")

output_dir = "/opt/airflow/data"
os.makedirs(output_dir, exist_ok=True)

# Données d'exemple (Météo)
data_weather = {
    "ville": ["Paris", "Marseille", "Lyon"],
    "temperature_celsius": [18.5, 24.0, 16.2],
    "condition": ["Pluie légère", "Ensoleillé", "Nuageux"],
    "date": [datetime.now().strftime("%Y-%m-%d")] * 3
}

df = pd.DataFrame(data_weather)
output_path = os.path.join(output_dir, "raw_weather.csv")
df.to_csv(output_path, index=False)

print(f"Ingestion Météo réussie ! Fichier sauvegardé dans : {output_path}")