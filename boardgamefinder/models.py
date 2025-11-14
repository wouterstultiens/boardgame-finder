from datetime import datetime
from typing import List, Literal
from pydantic import BaseModel, HttpUrl
from pydantic import Field

class BGGData(BaseModel):
    link: HttpUrl
    name: str
    year_published: int
    weight: float
    rating: float


class Game(BaseModel):
    llm_name: str
    llm_lang: Literal['nl', 'en', 'unknown']
    bgg_data: List[BGGData] = Field(default_factory=list)


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
    image_texts: List[str] = Field(default_factory=list)
    games: List[Game] = Field(default_factory=list)

    def __str__(self):
        return self.model_dump_json(indent=2)