from pathlib import Path

# Root del proyecto
BASE_DIR = Path(__file__).resolve().parent.parent.parent  # sube a la raíz Bets-GG-2026

# Database
DB_PATH = BASE_DIR / "data" / "football_stats.db"

# Crear carpeta si no existe
DB_PATH.parent.mkdir(parents=True, exist_ok=True)
