from datetime import datetime
from turtle import st
from typing import List, Optional
from pydantic import BaseModel, HttpUrl
from pydantic import Field

class BGGData(BaseModel):
    id: str
    name: str
    description: str
    year_published: int
    weight: float
    rating: float


class Game(BaseModel):
    llm_name: str
    bgg_name: List[BGGData] = Field(default_factory=list)

    def apply_bgg_row(self, row):
        self.bgg_name.append(
            BGGData(
                id=str(row["BGGId"]),
                name=row["Name"],
                description=row["Description"],
                year_published=int(row["YearPublished"]),
                weight=float(row["GameWeight"]),
                rating=float(row["AvgRating"]),
            )
        )


class Listing(BaseModel):
    title: str
    description: str
    price: float
    price_type: str
    link: HttpUrl
    city: str
    distance_km: int
    date: datetime
    images: List[HttpUrl] = Field(default_factory=list)
    games: List[Game] = Field(default_factory=list)

    def extract_games(self, llm) -> None:
        """
        Fills `self.games.llm_name` using an LLM.
        """
        names = llm.extract_names(
            title=self.title,
            description=self.description
        )
        self.games = [Game(llm_name=name) for name in names]

    def __str__(self):
        return self.model_dump_json(indent=2)
