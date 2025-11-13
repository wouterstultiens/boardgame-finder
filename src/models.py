from datetime import datetime
from typing import List
from pydantic import BaseModel, HttpUrl

class Listing(BaseModel):
    title: str
    description: str
    price: float
    price_type: str
    link: HttpUrl
    city: str
    distance: int
    date: datetime
    images: List[HttpUrl] = []

    def __str__(self):
        return self.model_dump_json(indent=2)