from src.api.api_football import APIFootballAdapter
from src.db.repositories import (
    LeagueRepository,
    TeamRepository,
    FixtureRepository,
    MatchStatsRepository,
    TeamMatchContextRepository
)
from src.utils.logger import get_logger

class IngestionPipeline:

    def __init__(self, api_key: str):
        self.logger = get_logger("INGESTION_PIPELINE")

        self.adapter = APIFootballAdapter(api_key)

        self.league_repo = LeagueRepository()
        self.team_repo = TeamRepository()
        self.fixture_repo = FixtureRepository()
        self.stats_repo = MatchStatsRepository()
        self.team_context_repo = TeamMatchContextRepository()

    TARGET_LEAGUES = [
        {"league_id": 39, "season": 2025},  # Premier League
        {"league_id": 140, "season": 2025}, # La Liga
        {"league_id": 135, "season": 2025}, # Serie A
        {"league_id": 78, "season": 2025},  # Bundesliga
        {"league_id": 61, "season": 2025},  # Ligue 1
]

    def run(self):
        self.logger.info("Pipeline de ingesta iniciado")

        for league_cfg in TARGET_LEAGUES:
            league_id = league_cfg["league_id"]
            season = league_cfg["season"]

            self.logger.info(f"Ingestando liga {league_id} temporada {season}")

            self._ingest_league(league_id, season)

        self.logger.info("Pipeline de ingesta finalizado")

    def _ingest_league(self, league_external_id: int, season: int):
        fixtures = self.adapter.get_fixtures(league_external_id, season)

        self.logger.info(f"{len(fixtures)} partidos encontrados")

        for fixture in fixtures:
            if self.fixture_repo.fixture_exists(fixture.external_id):
                continue

            self._process_fixture(fixture)

    def _process_fixture(self, fixture):
        self.logger.info(f"Procesando fixture {fixture.external_id}")

        # Guardar equipos
        home_team_id = self._upsert_team(fixture.home_team_external_id)
        away_team_id = self._upsert_team(fixture.away_team_external_id)

        # Guardar fixture
        self.fixture_repo.insert_fixture(
            external_id=fixture.external_id,
            league_id=fixture.league_external_id,
            date=fixture.date,
            home_team_id=home_team_id,
            away_team_id=away_team_id,
            status=fixture.status
        )

        # Guardar estadísticas si terminó
        if fixture.status == "FT":
            self._process_stats(fixture.external_id, home_team_id, away_team_id)

    def _upsert_team(self, team_external_id: int):
        self.team_repo.insert_team(
            external_id=team_external_id,
            name=str(team_external_id),
            country="UNKNOWN"
        )
        return self.team_repo.get_team_id(team_external_id)

    def _process_stats(self, fixture_external_id, home_team_id, away_team_id):
        stats = self.adapter.get_match_stats(fixture_external_id)

        self.stats_repo.insert_match_stats(
            fixture_id=fixture_external_id,
            corners_home=stats.corners_home,
            corners_away=stats.corners_away,
            yellows_home=stats.yellows_home,
            yellows_away=stats.yellows_away,
            goals_1H_home=stats.goals_1H_home,
            goals_1H_away=stats.goals_1H_away,
            goals_FT_home=stats.goals_FT_home,
            goals_FT_away=stats.goals_FT_away
        )

        self._insert_team_context(
            fixture_external_id,
            home_team_id,
            away_team_id,
            stats
        )

    def _insert_team_context(self, fixture_id, home_team_id, away_team_id, stats):

        # HOME
        self.team_context_repo.insert_team_context(
            fixture_id,
            home_team_id,
            True,
            stats.corners_home, stats.corners_away,
            stats.yellows_home, stats.yellows_away,
            stats.goals_1H_home, stats.goals_1H_away
        )

        # AWAY
        self.team_context_repo.insert_team_context(
            fixture_id,
            away_team_id,
            False,
            stats.corners_away, stats.corners_home,
            stats.yellows_away, stats.yellows_home,
            stats.goals_1H_away, stats.goals_1H_home
        )
