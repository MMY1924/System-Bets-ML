import pandas as pd
import sqlite3


class BaseFeatureBuilder:

    def __init__(self, db_path: str):
        self.db_path = db_path

    def load_team_match_context(self) -> pd.DataFrame:
        query = """
        SELECT
            tmc.team_id,
            tmc.fixture_id,
            f.date,
            tmc.is_home,
            tmc.corners_for,
            tmc.corners_against,
            tmc.yellows_for,
            tmc.yellows_against,
            tmc.goals_1H_for,
            tmc.goals_1H_against
        FROM team_match_context tmc
        JOIN fixtures f ON f.fixture_id = tmc.fixture_id
        ORDER BY tmc.team_id, f.date
        """

        with sqlite3.connect(self.db_path) as conn:
            df = pd.read_sql(query, conn)

        df["date"] = pd.to_datetime(df["date"])
        return df
