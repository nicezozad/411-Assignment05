from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from sqlmodel import Field, Session, SQLModel, create_engine, select

class TripDB(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
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
    id: int

app = FastAPI()

@app.get("/trips/{trip_id}")
async def read_trip_by_id(trip_id: int) -> TripOut:
    with Session(engine) as session:
        statement = select(TripDB).where(TripDB.id == trip_id)
        trip = session.exec(statement).first()

        if trip != None:
            print(trip)
            return trip
        
    raise HTTPException(
        status_code=404,
        detail="Trip id not found"
    )


#ไล่แต่ละ record
def insert_trip():
    trip_1 = TripDB(name='karamucho', destination='Home', duration=3,
                    price=100.0, group_size=1)
    trip_2 = TripDB(name='jojo', destination='Somewhere', duration=1,
                    price=500.0, group_size=26)
    trip_3 = TripDB(name='osaka', destination='Paradise', duration=999,
                    price=1.0, group_size=2)

    with Session(engine) as session:
        session.add(trip_1)
        session.add(trip_2)
        session.add(trip_3)
        session.commit()

