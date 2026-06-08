import os
import pandas as pd
from datetime import datetime

print("Démarrage de l'ingestion des données Football...")

output_dir = "/opt/airflow/data"
os.makedirs(output_dir, exist_ok=True)

data_football = {
    "match_id": [1, 2, 3],
    "equipe_domicile": ["Paris SG", "Marseille", "Lyon"],
    "equipe_exterieur": ["Monaco", "Lille", "Lens"],
    "score_domicile": [2, 1, 0],
    "score_exterieur": [1, 1, 2],
    "date": [datetime.now().strftime("%Y-%m-%d")] * 3
}

df = pd.DataFrame(data_football)
output_path = os.path.join(output_dir, "raw_football.csv")
df.to_csv(output_path, index=False)

print(f"Ingestion Football réussie ! Fichier sauvegardé dans : {output_path}")