from typing import Optional, List
from pydantic import BaseModel
from sqlmodel import Field, SQLModel, Relationship

# ---------- New: Line (สาย) ----------
class Line(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name_th: str
    name_en: str
    services: List["Service"] = Relationship(back_populates="line")

# ---------- Core Tables ----------
class Station(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name_th: str
    name_en: str

class Service(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    line_id: int = Field(foreign_key="line.id")
    code: str                         # COMMUTER 303, RAPID 111, ฯลฯ
    origin: str                       # BANGKOK หรือ KRUNG THEP APHIWAT CENTRAL TERMINAL
    direction: str                    # outbound / inbound

    line: Line = Relationship(back_populates="services")
    stops: List["ServiceStop"] = Relationship(back_populates="service")
    cars: List["ServiceCar"] = Relationship(back_populates="service")

class ServiceStop(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    service_id: int = Field(foreign_key="service.id")
    station_id: int = Field(foreign_key="station.id")
    stop_order: int

    service: Service = Relationship(back_populates="stops")
    station: Station = Relationship()

class ServiceCar(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    service_id: int = Field(foreign_key="service.id")
    car_type: str
    car_count: int
    seats_per_car: int
    reserved_seats: int = 0

    service: Service = Relationship(back_populates="cars")

    @property
    def total_seats(self) -> int:
        return self.car_count * self.seats_per_car

    @property
    def available_seats(self) -> int:
        return self.total_seats - self.reserved_seats

class Ticket(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    service_id: int = Field(foreign_key="service.id")
    car_type: str
    quantity: int

# ---------- Schemas ----------
class StationOut(BaseModel):
    id: int
    name_th: str
    name_en: str

class ServiceStopOut(BaseModel):
    order: int
    station: StationOut

class ServiceCarIn(BaseModel):
    car_type: str
    car_count: int
    seats_per_car: int

class ServiceCarOut(ServiceCarIn):
    total_seats: int
    reserved_seats: int
    available_seats: int

class ServiceCreate(BaseModel):
    line_id: int
    code: str
    origin: str
    direction: str
    stop_station_ids_in_order: List[int]
    cars: List[ServiceCarIn]

class ServiceBasicOut(BaseModel):
    id: int
    line_id: int
    code: str
    origin: str
    direction: str

class ServiceDetailOut(ServiceBasicOut):
    stops: List[ServiceStopOut]
    cars: List[ServiceCarOut]

class TicketRequest(BaseModel):
    service_id: int
    car_type: str
    quantity: int

class TicketOut(BaseModel):
    id: int
    service_id: int
    car_type: str
    quantity: int

class SeatQuery(BaseModel):
    service_id: int
    car_type: str

class LineCreate(BaseModel):
    name_th: str
    name_en: str

class LineOut(BaseModel):
    id: int
    name_th: str
    name_en: str
