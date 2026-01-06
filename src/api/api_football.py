import requests
from datetime import datetime
from src.api.base_adapter import FootballAPIAdapter
from src.api.models import League, Team, Fixture, MatchStats


class APIFootballAdapter(FootballAPIAdapter):

    BASE_URL = "https://v3.football.api-sports.io"

    def __init__(self, api_key: str):
        self.headers = {"x-apisports-key": api_key}

    def _get(self, endpoint: str, params: dict = None):
        response = requests.get(
            f"{self.BASE_URL}/{endpoint}",
            headers=self.headers,
            params=params
        )
        response.raise_for_status()
        return response.json()["response"]

    def get_leagues(self):
        data = self._get("leagues")
        leagues = []

        for item in data:
            league = item["league"]
            country = item["country"]

            for season in item["seasons"]:
                leagues.append(
                    League(
                        external_id=league["id"],
                        name=league["name"],
                        country=country["name"],
                        season=season["year"]
                    )
                )

        return leagues

    def get_fixtures(self, league_external_id: int, season: int):
        data = self._get(
            "fixtures",
            params={"league": league_external_id, "season": season}
        )

        fixtures = []
        for item in data:
            fixture = item["fixture"]
            teams = item["teams"]

            fixtures.append(
                Fixture(
                    external_id=fixture["id"],
                    league_external_id=league_external_id,
                    date=datetime.fromisoformat(fixture["date"].replace("Z", "")),
                    home_team_external_id=teams["home"]["id"],
                    away_team_external_id=teams["away"]["id"],
                    status=fixture["status"]["short"]
                )
            )

        return fixtures

    def get_match_stats(self, fixture_external_id: int):
        data = self._get("fixtures/statistics", params={"fixture": fixture_external_id})

        home = data[0]["statistics"]
        away = data[1]["statistics"]

        def get_stat(stats, name):
            for s in stats:
                if s["type"] == name:
                    return s["value"] or 0
            return 0

        return MatchStats(
            fixture_external_id=fixture_external_id,
            corners_home=get_stat(home, "Corner Kicks"),
            corners_away=get_stat(away, "Corner Kicks"),
            yellows_home=get_stat(home, "Yellow Cards"),
            yellows_away=get_stat(away, "Yellow Cards"),
            goals_1H_home=get_stat(home, "Goals"),
            goals_1H_away=get_stat(away, "Goals"),
            goals_FT_home=get_stat(home, "Goals"),
            goals_FT_away=get_stat(away, "Goals")
        )
