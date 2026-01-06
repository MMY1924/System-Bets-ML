from src.db.connection import get_connection


class BaseRepository:
    def __init__(self):
        self.conn = get_connection()
        self.cursor = self.conn.cursor()

    def commit(self):
        self.conn.commit()

    def close(self):
        self.conn.close()

class LeagueRepository(BaseRepository):

    def insert_league(self, external_id, name, country, season, start_date=None, end_date=None):
        self.cursor.execute("""
        INSERT OR IGNORE INTO leagues (
            external_league_id, name, country, season, start_date, end_date
        )
        VALUES (?, ?, ?, ?, ?, ?)
        """, (external_id, name, country, season, start_date, end_date))
        self.commit()

    def get_league_id(self, external_id):
        self.cursor.execute("""
        SELECT league_id FROM leagues WHERE external_league_id = ?
        """, (external_id,))
        row = self.cursor.fetchone()
        return row["league_id"] if row else None
class TeamRepository(BaseRepository):

    def insert_team(self, external_id, name, country):
        self.cursor.execute("""
        INSERT OR IGNORE INTO teams (
            external_team_id, name, country
        )
        VALUES (?, ?, ?)
        """, (external_id, name, country))
        self.commit()

    def get_team_id(self, external_id):
        self.cursor.execute("""
        SELECT team_id FROM teams WHERE external_team_id = ?
        """, (external_id,))
        row = self.cursor.fetchone()
        return row["team_id"] if row else None
    
class TeamRepository(BaseRepository):

    def insert_team(self, external_id, name, country):
        self.cursor.execute("""
        INSERT OR IGNORE INTO teams (
            external_team_id, name, country
        )
        VALUES (?, ?, ?)
        """, (external_id, name, country))
        self.commit()

    def get_team_id(self, external_id):
        self.cursor.execute("""
        SELECT team_id FROM teams WHERE external_team_id = ?
        """, (external_id,))
        row = self.cursor.fetchone()
        return row["team_id"] if row else None

class FixtureRepository(BaseRepository):

    def fixture_exists(self, external_fixture_id):
        self.cursor.execute("""
        SELECT 1 FROM fixtures WHERE external_fixture_id = ?
        """, (external_fixture_id,))
        return self.cursor.fetchone() is not None

    def insert_fixture(self, external_id, league_id, date, home_team_id, away_team_id, status):
        self.cursor.execute("""
        INSERT OR IGNORE INTO fixtures (
            external_fixture_id, league_id, date,
            home_team_id, away_team_id, status
        )
        VALUES (?, ?, ?, ?, ?, ?)
        """, (external_id, league_id, date, home_team_id, away_team_id, status))
        self.commit()

    def get_fixture_id(self, external_fixture_id):
        self.cursor.execute("""
        SELECT fixture_id FROM fixtures WHERE external_fixture_id = ?
        """, (external_fixture_id,))
        row = self.cursor.fetchone()
        return row["fixture_id"] if row else None

class MatchStatsRepository(BaseRepository):

    def insert_match_stats(
        self,
        fixture_id,
        corners_home, corners_away,
        yellows_home, yellows_away,
        goals_1H_home, goals_1H_away,
        goals_FT_home, goals_FT_away
    ):
        self.cursor.execute("""
        INSERT OR REPLACE INTO match_stats VALUES (
            ?, ?, ?, ?, ?, ?, ?, ?, ?
        )
        """, (
            fixture_id,
            corners_home, corners_away,
            yellows_home, yellows_away,
            goals_1H_home, goals_1H_away,
            goals_FT_home, goals_FT_away
        ))
        self.commit()

class TeamMatchContextRepository(BaseRepository):

    def insert_team_context(
        self,
        fixture_id,
        team_id,
        is_home,
        corners_for, corners_against,
        yellows_for, yellows_against,
        goals_1H_for, goals_1H_against
    ):
        self.cursor.execute("""
        INSERT OR REPLACE INTO team_match_context VALUES (
            ?, ?, ?, ?, ?, ?, ?, ?, ?
        )
        """, (
            fixture_id, team_id, is_home,
            corners_for, corners_against,
            yellows_for, yellows_against,
            goals_1H_for, goals_1H_against
        ))
        self.commit()
