import datetime
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
    date: datetime
    images: List[ListingImage] = Field(default_factory=list)