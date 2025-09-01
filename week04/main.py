from typing import List
from fastapi import FastAPI, HTTPException
from sqlmodel import Session, select
from database import engine, init_db
from model import TripDB, Trip, TripOut, TripFilter

init_db()
app = FastAPI()

@app.get("/trips/{trip_id}")
async def read_trip(trip_id: int) -> TripOut:
    with Session(engine) as session:
        trip = session.get(TripDB, trip_id)

        if trip != None:
            print(trip)
            return trip
        
    raise HTTPException(
        status_code=404,
        detail="Trip not found"
    )

@app.post("/trips/")
async def read_filtered_trip(filter: TripFilter) -> List[TripOut]:
    with Session(engine) as session:
        statement = select(TripDB) \
            .where(TripDB.duration >= filter.duration) \
            .where(TripDB.group_size >= filter.group_size)
        all_trip = session.exec(statement).all()

        if all_trip != None:
            print(all_trip)
            return all_trip
        
    raise HTTPException(
        status_code=404,
        detail="Trip not found"
    )

def insert_trip():
    trip_1 = TripDB(name="W&T 001", destination='Florida', 
                    duration=50, price=160000, group_size=1)
    trip_2 = TripDB(name="W&T 002", destination='Alaska', 
                    duration=60, price=160000, group_size=1)
    trip_3 = TripDB(name="Aekarin", destination='lao', 
                    duration=70, price=160000, group_size=1)
    trip_4 = TripDB(name="John", destination='Bangkok', 
                    duration=80, price=160000, group_size=1)

    with Session(engine) as session:
        session.add(trip_3)
        session.add(trip_4)
        session.commit()

if __name__ == "__main__":
    insert_trip()  