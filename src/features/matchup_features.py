import pandas as pd


class MatchupFeatureBuilder:

    def build_matchup_features(self, df: pd.DataFrame) -> pd.DataFrame:
        df = df.copy()

        home = df[df["is_home"] == 1]
        away = df[df["is_home"] == 0]

        matchup = home.merge(
            away,
            on="fixture_id",
            suffixes=("_home", "_away")
        )

        matchup["delta_avg_corners_5"] = (
            matchup["avg_corners_for_5_home"] -
            matchup["avg_corners_for_5_away"]
        )

        matchup["delta_yellows_5"] = (
            matchup["avg_yellows_for_5_home"] -
            matchup["avg_yellows_for_5_away"]
        )

        matchup["expected_total_corners"] = (
            matchup["avg_corners_for_5_home"] +
            matchup["avg_corners_for_5_away"]
        )

        return matchup


