from typing import Optional
from sqlmodel import Field, Session, SQLModel, create_engine,select
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

class TripDB(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str
    destination: str
    duration: int
    price: float
    group_size: int

engine = create_engine("sqlite:///data.db")
SQLModel.metadata.create_all(engine)

class Trip(BaseModel):
    name: str
    destination: str
    duration: int
    price: float
    group_size: int

class TripOut(Trip):
    id:int

app = FastAPI()

@app.get("/trips/{trip_id}")
async def read_trip(trip_id: int) -> TripOut:
    with Session(engine) as session:
        statement = select(TripDB).where(TripDB.id == trip_id)
        trip = session.exec(statement).first()

        if trip != None:
            print(trip)
            return trip
        raise HTTPException(
            status_code=404,
            detail="Trip is not found"
        )

def insert_trip():
    trip_1 = TripDB(name="W&T 001", destination='Florida', 
                    duration=60, price=160000, group_size=1)
    trip_2 = TripDB(name="W&T 002", destination='Alaska', 
                    duration=60, price=160000, group_size=1)

    with Session(engine) as session:
        session.add(trip_1)
        session.add(trip_2)
        session.commit()

with Session(engine) as session:
    statement = select(TripDB).where(TripDB.id == 2)
    trip = session.exec(statement).first()
    print(trip)