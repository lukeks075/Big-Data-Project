import os

BASE = "datalake"

dirs = [
    f"{BASE}/raw/football/fixtures",
    f"{BASE}/raw/football/players_stats",
    f"{BASE}/raw/weather",
    f"{BASE}/formatted/stg_players",
    f"{BASE}/formatted/stg_weather",
    f"{BASE}/usage/injury_risk_score",
    "logs",
]

for d in dirs:
    os.makedirs(d, exist_ok=True)
    open(os.path.join(d, ".gitkeep"), "w").close()

for root, subdirs, files in os.walk(BASE):
    level = root.replace(BASE, "").count(os.sep)
    indent = "  " * level
    print(f"{indent}{os.path.basename(root)}/")