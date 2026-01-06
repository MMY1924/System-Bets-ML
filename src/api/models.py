from dataclasses import dataclass
from datetime import datetime


@dataclass
class League:
    external_id: int
    name: str
    country: str
    season: int


@dataclass
class Team:
    external_id: int
    name: str
    country: str


@dataclass
class Fixture:
    external_id: int
    league_external_id: int
    date: datetime
    home_team_external_id: int
    away_team_external_id: int
    status: str


@dataclass
class MatchStats:
    fixture_external_id: int
    corners_home: int
    corners_away: int
    yellows_home: int
    yellows_away: int
    goals_1H_home: int
    goals_1H_away: int
    goals_FT_home: int
    goals_FT_away: int
