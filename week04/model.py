from pydantic import BaseModel
from sqlmodel import Field, SQLModel
from typing import Optional

class Trip(BaseModel):
    name: str
    destination: str
    duration: int
    price: float
    group_size: int

class TripOut(Trip):
    id: int

class TripDB(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str
    destination: str
    duration: int
    price: float
    group_size: int

class TripFilter(BaseModel):
    duration: int
    group_size: int