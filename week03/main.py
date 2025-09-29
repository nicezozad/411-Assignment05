from datetime import date
from typing import Optional, Literal, List
from fastapi import FastAPI, HTTPException
from sqlmodel import Field, Session, select
from fastapi import FastAPI, HTTPException, Body
from data import engine, init_db
from model import PersonalDB, Personal,PersonalOut

app = FastAPI()

def insert_personal():
    p1 = PersonalDB(
        name="Nice", surname="Techai", user_type="individual",
        phone_number="095-000-0001", email="nice@example.com",
        idcard_file="id001.png", id_number="1234567890123",
        birth=date(2003, 1, 1), religion="Buddhism",
        village_name="Ban A", house_number="99/9",
        road="Main", alley="-", province="Bangkok",
        district="Pathumwan", subdistrict="Lumphini"
    )
    p2 = PersonalDB(
        name="Jojo", surname="Bravo", user_type="group",
        phone_number="095-000-0002", email="jojo@example.com",
        idcard_file="id002.png", id_number="2345678901234",
        birth=date(2002, 5, 12), religion="Christianity",
        village_name="Ban B", house_number="12/3",
        road="Second", alley="Soi 5", province="Chiang Mai",
        district="Mueang", subdistrict="Suthep"
    )
    p3 = PersonalDB(
        name="Alice", surname="Wong", user_type="individual",
        phone_number="095-000-0003", email="alice@example.com",
        idcard_file="id003.png", id_number="3456789012345",
        birth=date(2001, 9, 30), religion="None",
        village_name="Ban C", house_number="7",
        road="Third", alley="-", province="Phuket",
        district="Mueang", subdistrict="Talat Yai"
    )
    p4 = PersonalDB(
        name="Bob", surname="Smith", user_type="group",
        phone_number="095-000-0004", email="bob@example.com",
        idcard_file="id004.png", id_number="4567890123456",
        birth=date(1999, 12, 15), religion="Islam",
        village_name="Ban D", house_number="21/5",
        road="Fourth", alley="Soi 10", province="Khon Kaen",
        district="Mueang", subdistrict="Nai Mueang"
    )

    with Session(engine) as session:
        session.add_all([p1, p2, p3, p4])
        session.commit()

@app.post("/personal/bulk", response_model=List[PersonalOut], status_code=201)
def create_personal_bulk(items: List[Personal]):
    rows = []
    with Session(engine) as session:
        for it in items:                       # วน loop แต่ละ item ใน list
            row = PersonalDB(**it.model_dump()) # แปลง Pydantic → SQLModel
            session.add(row)                    # add เข้า session
            rows.append(row)                    # เก็บไว้คืนค่า response
        session.commit()                        # commit ทีเดียว
        for r in rows:
            session.refresh(r)                  # refresh ให้ได้ id ใหม่
    return rows

@app.get("/personal/by-id/{personal_id}", response_model=PersonalOut)
def read_personal(personal_id: int):
    with Session(engine) as session:
        person = session.get(PersonalDB, personal_id)
        if not person:
            raise HTTPException(status_code=404, detail="Personal is not found")
        return person
    
@app.delete("/personal/bulk")
def delete_many(ids: list[int] = Body(...)):
    with Session(engine) as session:
        for pid in ids:                       # วน loop id แต่ละตัว
            person = session.get(PersonalDB, pid)
            if person:                        # ถ้าเจอ record
                session.delete(person)        # mark ให้ลบ
        session.commit()                      # commit ทีเดียว
    return {"message": f"Deleted personals {ids}"}

@app.get("/personal/search", response_model=List[PersonalOut])
def search_personal(name: str):
    with Session(engine) as session:
        rows = session.exec(
            select(PersonalDB).where(PersonalDB.name.contains(name))
        ).all()
        if not rows:
            raise HTTPException(status_code=404, detail="No results")
        return rows

@app.delete("/personal/by-name/{name}")
def delete_personal_by_name(name: str):
    with Session(engine) as session:
        rows = session.exec(
            select(PersonalDB).where(PersonalDB.name == name)
        ).all()
        if not rows:
            raise HTTPException(status_code=404, detail="Name not found")
        for r in rows:
            session.delete(r)
        session.commit()
        return {"message": f"Deleted {len(rows)} record(s) with name '{name}'"}

def delete_personal(personal_id: int):
    with Session(engine) as session:
        person = session.get(PersonalDB, personal_id)
        if not person:
            print("Not found")
            return
        session.delete(person)
        session.commit()
        print(f"Deleted personal {personal_id}")

#with Session(engine) as session:
    #statement = select(PersonalDB).where(PersonalDB.id == 2)
    #person = session.exec(statement).first()
    #print(person)

def select_personal():
    with Session(engine) as session:
        statement = select(PersonalDB) \
            .where(PersonalDB.name == "Somchai") \
            .where(PersonalDB.phone_number == "0812345678")
        persons = session.exec(statement).all()   # ดึงทั้งหมดมาเป็น list
        if not persons:
            print("ไม่เจอข้อมูลที่ตรงเงื่อนไข")
        else:
            for person in persons:
                print(person)


if __name__ == "__main__":
    #insert_personal()   
    #delete_personal()
    select_personal()