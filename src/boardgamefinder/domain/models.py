# src/boardgamefinder/domain/models.py
from __future__ import annotations
from datetime import datetime
from typing import List, Literal, Optional
from pydantic import BaseModel, HttpUrl, Field

class BGGData(BaseModel):
    id: int
    link: HttpUrl
    name: str
    year_published: Optional[int] = None
    weight: Optional[float] = None
    rating: Optional[float] = None
    image_path: Optional[HttpUrl] = None

class Game(BaseModel):
    llm_name: str
    llm_lang: Literal['nl', 'en', 'unknown']
    bgg_data: Optional[BGGData] = None # A game can only match one BGG entry

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

    # Timestamps for tracking
    created_at: datetime = Field(default_factory=lambda: datetime.now())
    updated_at: datetime = Field(default_factory=lambda: datetime.now())

    def __str__(self):
        return self.model_dump_json(indent=2)