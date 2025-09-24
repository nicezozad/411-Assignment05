from __future__ import annotations
from typing import Optional
from datetime import datetime
from enum import Enum

from pydantic import BaseModel, Field
from sqlmodel import SQLModel, Field as SQLField


# ---------- Enums ----------
class DirectionEnum(str, Enum):
    outbound = "outbound"
    inbound = "inbound"

class CarTypeEnum(str, Enum):
    First = "First"
    Reserved = "Reserved"
    NonReserved = "Non-reserved"
    Quiet = "Quiet"
    Catering = "Catering"


# ---------- DB Models (NO Relationship fields) ----------
class Line(SQLModel, table=True):
    id: Optional[int] = SQLField(default=None, primary_key=True)
    name_th: str
    name_en: str

class Station(SQLModel, table=True):
    id: Optional[int] = SQLField(default=None, primary_key=True)
    name_th: str
    name_en: str

class Service(SQLModel, table=True):
    id: Optional[int] = SQLField(default=None, primary_key=True)
    line_id: int = SQLField(foreign_key="line.id", index=True)
    code: str
    origin: str
    direction: DirectionEnum
    departure_time: datetime
    arrival_time: datetime

class ServiceStop(SQLModel, table=True):
    id: Optional[int] = SQLField(default=None, primary_key=True)
    service_id: int = SQLField(foreign_key="service.id", index=True)
    station_id: int = SQLField(foreign_key="station.id", index=True)
    stop_order: int

class ServiceCar(SQLModel, table=True):
    id: Optional[int] = SQLField(default=None, primary_key=True)
    service_id: int = SQLField(foreign_key="service.id", index=True)
    car_type: CarTypeEnum
    car_count: int
    seats_per_car: int
    reserved_seats: int = 0
    version: int = 0  # optimistic locking

    @property
    def total_seats(self) -> int:
        return self.car_count * self.seats_per_car

    @property
    def available_seats(self) -> int:
        return self.total_seats - self.reserved_seats

class Ticket(SQLModel, table=True):
    id: Optional[int] = SQLField(default=None, primary_key=True)
    service_id: int = SQLField(foreign_key="service.id", index=True)
    car_type: CarTypeEnum
    quantity: int


# ---------- API Schemas ----------
class StationOut(BaseModel):
    id: int
    name_th: str
    name_en: str

class ServiceStopOut(BaseModel):
    order: int
    station: StationOut

class ServiceCarOut(BaseModel):
    car_type: CarTypeEnum
    car_count: int
    seats_per_car: int
    total_seats: int
    reserved_seats: int
    available_seats: int

class ServiceBasicOut(BaseModel):
    id: int
    line_id: int
    code: str
    origin: str
    direction: DirectionEnum
    departure_time: datetime
    arrival_time: datetime

class ServiceDetailOut(ServiceBasicOut):
    stops: list[ServiceStopOut]
    cars: list[ServiceCarOut]

class ServiceCreate(BaseModel):
    line_id: int
    code: str
    origin: str
    direction: DirectionEnum
    stop_station_ids: list[int] = Field(min_items=2)
    departure_time: Optional[datetime] = None
    arrival_time: Optional[datetime] = None

class TicketRequest(BaseModel):
    service_id: int = Field(gt=0)
    car_type: CarTypeEnum
    quantity: int = Field(ge=1, le=50)

class TicketOut(BaseModel):
    id: int
    service_id: int
    car_type: CarTypeEnum
    quantity: int
