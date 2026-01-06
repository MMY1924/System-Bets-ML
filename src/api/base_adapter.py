from abc import ABC, abstractmethod
from typing import List
from src.api.models import League, Team, Fixture, MatchStats


class FootballAPIAdapter(ABC):

    @abstractmethod
    def get_leagues(self) -> List[League]:
        pass

    @abstractmethod
    def get_teams(self, league_external_id: int) -> List[Team]:
        pass

    @abstractmethod
    def get_fixtures(self, league_external_id: int, season: int) -> List[Fixture]:
        pass

    @abstractmethod
    def get_match_stats(self, fixture_external_id: int) -> MatchStats:
        pass
