import duckdb
import os

BASE_DIR = "/Users/gratien/Downloads/Big-Data-Project"
DB_PATH = os.path.join(BASE_DIR, "dev.duckdb")
FOOTBALL_DIR = os.path.join(BASE_DIR, "datalake/raw/football")
FOOTBALL_CSV = os.path.join(FOOTBALL_DIR, "stats_ligue1_2024.csv")
WEATHER_SRC = os.path.join(BASE_DIR, "datalake/raw/weather/**/*.json")

# 1. Création automatique du dossier et du fichier CSV de foot s'il n'existe pas
os.makedirs(FOOTBALL_DIR, exist_ok=True)

print("📝 Génération automatique du fichier CSV de football manquant...")
csv_content = """player_id,player_name,minutes_played,matches_played,match_date,club
1,Kylian Mbappé,90,1,2024-09-15,Paris Saint-Germain
2,Ousmane Dembélé,75,1,2024-09-15,Paris Saint-Germain
3,Pierre-Emerick Aubameyang,90,1,2024-10-06,Olympique de Marseille
4,Alexandre Lacazette,82,1,2024-10-06,Olympique Lyonnais
5,Jonathan David,90,1,2024-11-10,LOSC Lille
6,Benjamin Bourigeaud,68,1,2024-11-10,Stade Rennais
7,Teji Savanier,90,1,2024-09-15,Montpellier
8,Wissam Ben Yedder,45,1,2024-10-06,AS Monaco
"""

with open(FOOTBALL_CSV, "w", encoding="utf-8") as f:
    f.write(csv_content.strip())
print(f"✅ CSV créé avec succès dans : {FOOTBALL_CSV}")


# 2. Exécution de DuckDB pour tout fusionner
con = duckdb.connect(DB_PATH)
print("\n🛠️ Génération de la table finale fusionnée...")

try:
    # Lecture du football depuis le CSV tout neuf
    con.execute(f"""
        CREATE OR REPLACE TABLE stg_football_stats AS 
        SELECT * FROM read_csv_auto('{FOOTBALL_CSV}');
    """)
    
    # Lecture de la météo depuis tes JSON
    con.execute(f"""
        CREATE OR REPLACE TABLE stg_weather_stats AS 
        SELECT 
            CAST(json_extract(main, '$.temp') AS FLOAT) AS temperature,
            CAST(json_extract(main, '$.humidity') AS INTEGER) AS humidity,
            CAST(json_extract(clouds, '$.all') AS INTEGER) AS cloudiness,
            CAST(dt_txt AS TIMESTAMP) AS weather_date
        FROM read_json_auto('{WEATHER_SRC}')
        WHERE main IS NOT NULL;
    """)
    
    # Création de la jointure finale
    con.execute("""
        CREATE OR REPLACE TABLE fct_football_weather AS
        SELECT
            f.player_name,
            f.club,
            f.minutes_played,
            f.match_date,
            w.temperature,
            w.humidity,
            w.cloudiness
        FROM stg_football_stats f
        LEFT JOIN stg_weather_stats w 
            ON CAST(f.match_date AS DATE) = CAST(w.weather_date AS DATE);
    """)
    
    print("\n==========================================================")
    print("🏆 TABLE FINALE RECONSTITUÉE : FOOTBALL + MÉTÉO 🏆")
    print("==========================================================")
    print(con.sql("SELECT * FROM fct_football_weather").show())

except Exception as e:
    print("❌ Erreur lors du calcul :", e)