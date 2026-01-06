from pathlib import Path

#Project Root
BASE_DIR = Path(__file__).resolve().parents[2]

#Database
DB_PATH = BASE_DIR / "data" / "football_stats.db"

#Ingestion
INGESTION_TIMEZONE = "UTC"

#Logging
LOG_DIR = BASE_DIR / "logs"

#Leagues
TARGET_LEAGUES = [
    "PREMIER_LEAGUE",
    "LALIGA",
    "SERIE A",
    "BUNDENSLIGA",
    "LIGUE_1"
]

SEASON = "2025"
