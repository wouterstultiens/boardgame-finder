from datetime import datetime
from typing import List, Optional
from pydantic import BaseModel, HttpUrl
from pydantic import Field


class Game(BaseModel):
    llm_name: str
    bgg_name: Optional[str] = None


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

    def __str__(self):
        return self.model_dump_json(indent=2)
