from src.features.base_features import BaseFeatureBuilder
from src.features.rolling_features import RollingFeatureBuilder
from src.features.home_away_features import HomeAwayFeatureBuilder
from src.features.matchup_features import MatchupFeatureBuilder

DB_PATH = "data/football.db"

def main():
    print("🔹 Cargando datos base...")
    base = BaseFeatureBuilder(DB_PATH)
    df = base.load_team_match_context()

    print(f"Filas cargadas: {len(df)}")
    print(df.head())

    print("\n🔹 Generando rolling features...")
    df = RollingFeatureBuilder().add_rolling_features(df)

    print("\n🔹 Generando home/away features...")
    df = HomeAwayFeatureBuilder().add_home_away_features(df)

    print("\n🔹 Generando matchup features...")
    matchup_df = MatchupFeatureBuilder().build_matchup_features(df)

    print("\n✅ DATASET FINAL")
    print(f"Filas: {len(matchup_df)}")
    print(f"Columnas: {len(matchup_df.columns)}")

    print("\n🔍 Sample:")
    print(matchup_df.head())

    print("\n📊 Descriptivo rápido (corners):")
    print(matchup_df[
        ["avg_corners_for_5_home", "avg_corners_for_5_away", "expected_total_corners"]
    ].describe())

if __name__ == "__main__":
    main()

