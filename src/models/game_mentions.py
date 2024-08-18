from enum import Enum


from pydantic import BaseModel
from datetime import date, datetime
from typing import List


class GameMention(BaseModel):
    source: str
    date: datetime
    description: str
    url: str


class MentionSummary(BaseModel):
    date: date
    count: int
    mentions: List[GameMention]


class StatsModel(BaseModel):
    date: str
    followers: int


class Response(BaseModel):
    total_results: int
    results: List[MentionSummary]
    stats: list[StatsModel]


class DateRangeEnum(str, Enum):
    week = "week"
    month = "month"
    three_months = "three_months"
    six_months = "six_months"
    year = "year"
