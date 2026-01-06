from src.db.connection import get_connection


def create_tables():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS leagues (
        league_id INTEGER PRIMARY KEY AUTOINCREMENT,
        external_league_id TEXT UNIQUE,
        name TEXT,
        country TEXT,
        season TEXT,
        start_date TEXT,
        end_date TEXT
    )
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS teams (
        team_id INTEGER PRIMARY KEY AUTOINCREMENT,
        external_team_id TEXT UNIQUE,
        name TEXT,
        country TEXT
    )
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS league_teams (
        league_id INTEGER,
        team_id INTEGER,
        PRIMARY KEY (league_id, team_id)
    )
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS fixtures (
        fixture_id INTEGER PRIMARY KEY AUTOINCREMENT,
        external_fixture_id TEXT UNIQUE,
        league_id INTEGER,
        date TEXT,
        home_team_id INTEGER,
        away_team_id INTEGER,
        status TEXT
    )
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS match_stats (
        fixture_id INTEGER PRIMARY KEY,
        corners_home INTEGER,
        corners_away INTEGER,
        yellows_home INTEGER,
        yellows_away INTEGER,
        goals_1H_home INTEGER,
        goals_1H_away INTEGER,
        goals_FT_home INTEGER,
        goals_FT_away INTEGER
    )
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS team_match_context (
        fixture_id INTEGER,
        team_id INTEGER,
        is_home INTEGER,
        corners_for INTEGER,
        corners_against INTEGER,
        yellows_for INTEGER,
        yellows_against INTEGER,
        goals_1H_for INTEGER,
        goals_1H_against INTEGER,
        PRIMARY KEY (fixture_id, team_id)
    )
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS ingestion_log (
        run_date TEXT,
        fixtures_processed INTEGER,
        api_requests_used INTEGER,
        status TEXT,
        error_message TEXT
    )
    """)

    conn.commit()
    conn.close()
