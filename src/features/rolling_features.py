import pandas as pd


class RollingFeatureBuilder:

    def __init__(self, windows=(3, 5, 10)):
        self.windows = windows

    def add_rolling_features(self, df: pd.DataFrame) -> pd.DataFrame:
        df = df.copy()

        for w in self.windows:
            df[f"avg_corners_for_{w}"] = (
                df.groupby("team_id")["corners_for"]
                .rolling(w, min_periods=1)
                .mean()
                .reset_index(level=0, drop=True)
            )

            df[f"avg_yellows_for_{w}"] = (
                df.groupby("team_id")["yellows_for"]
                .rolling(w, min_periods=1)
                .mean()
                .reset_index(level=0, drop=True)
            )

            df[f"std_corners_for_{w}"] = (
                df.groupby("team_id")["corners_for"]
                .rolling(w, min_periods=1)
                .std()
                .reset_index(level=0, drop=True)
                .fillna(0)
            )

            df[f"trend_corners_{w}"] = (
                df.groupby("team_id")["corners_for"]
                .rolling(w, min_periods=2)
                .apply(lambda x: x.iloc[-1] - x.iloc[0], raw=False)
                .reset_index(level=0, drop=True)
                .fillna(0)
            )

        return df

