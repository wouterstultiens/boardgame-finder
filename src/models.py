from datetime import datetime
from typing import List
from pydantic import BaseModel, Field, HttpUrl

class ListingImage(BaseModel):
    url: HttpUrl

class Listing(BaseModel):
    title: str
    description: str
    price: float
    price_type: str
    link: HttpUrl
    city: str
    distance: int
    date: datetime
    images: List[ListingImage] = Field(default_factory=list)

    def __repr__(self):
        return self.model_dump_json(indent=2)