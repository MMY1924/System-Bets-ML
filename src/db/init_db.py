print("🟢 Iniciando init_db.py")  # debug inicio

from src.db.connection import get_connection

print("🟢 Import de get_connection OK")  # debug después del import

def init_db():
    print("🟢 Llamando a get_connection()")  # debug antes de abrir conexión
    conn = get_connection()
    cursor = conn.cursor()
    print("🟢 Conexión establecida, creando tablas...")

    # ---------- LEAGUES ----------
    print("🟢 Creando tabla leagues...")
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS leagues (
        league_id INTEGER PRIMARY KEY,
        name TEXT NOT NULL,
        country TEXT,
        season TEXT
    );
    """)

    # ---------- TEAMS ----------
    print("🟢 Creando tabla teams...")
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS teams (
        team_id INTEGER PRIMARY KEY,
        name TEXT NOT NULL,
        league_id INTEGER,
        FOREIGN KEY (league_id) REFERENCES leagues (league_id)
    );
    """)

    # ---------- FIXTURES ----------
    print("🟢 Creando tabla fixtures...")
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS fixtures (
        fixture_id INTEGER PRIMARY KEY,
        date TEXT NOT NULL,
        league_id INTEGER,
        home_team_id INTEGER,
        away_team_id INTEGER,
        FOREIGN KEY (league_id) REFERENCES leagues (league_id),
        FOREIGN KEY (home_team_id) REFERENCES teams (team_id),
        FOREIGN KEY (away_team_id) REFERENCES teams (team_id)
    );
    """)

    # ---------- TEAM MATCH STATS ----------
    print("🟢 Creando tabla team_match_stats...")
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS team_match_stats (
        fixture_id INTEGER,
        team_id INTEGER,
        is_home INTEGER,
        corners INTEGER,
        yellow_cards INTEGER,
        goals_first_half INTEGER,
        PRIMARY KEY (fixture_id, team_id),
        FOREIGN KEY (fixture_id) REFERENCES fixtures (fixture_id),
        FOREIGN KEY (team_id) REFERENCES teams (team_id)
    );
    """)

    conn.commit()
    conn.close()
    print("✅ DB y tablas inicializadas correctamente")


if __name__ == "__main__":
    print("🟢 Ejecutando init_db()")
    init_db()
    print("🟢 init_db.py terminado")
