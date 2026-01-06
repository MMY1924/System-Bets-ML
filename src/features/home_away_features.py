import pandas as pd


class HomeAwayFeatureBuilder:

    def add_home_away_features(self, df: pd.DataFrame) -> pd.DataFrame:
        df = df.copy()

        for location in [True, False]:
            suffix = "home" if location else "away"

            mask = df["is_home"] == location

            df.loc[mask, f"avg_corners_{suffix}_5"] = (
                df[mask]
                .groupby("team_id")["corners_for"]
                .rolling(5, min_periods=1)
                .mean()
                .reset_index(level=0, drop=True)
            )

            df.loc[mask, f"avg_yellows_{suffix}_5"] = (
                df[mask]
                .groupby("team_id")["yellows_for"]
                .rolling(5, min_periods=1)
                .mean()
                .reset_index(level=0, drop=True)
            )

        df.fillna(0, inplace=True)
        return df
