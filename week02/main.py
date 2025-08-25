from fastapi import FastAPI
from pydantic import BaseModel, EmailStr
from typing import Literal
from datetime import date

class Personal(BaseModel):
    name: str
    surname: str
    user_type: Literal["individual", "group"]
    phone_number: str
    email: EmailStr
    idcard_file: str
    id_number: str
    birth: date
    religion: str
    village_name: str
    house_number: str
    road: str
    alley: str
    province: str
    district: str
    subdistrict: str

class PersonalOut(Personal):
    id: int

app = FastAPI()

personal_db = []

@app.post("/personal/")
async def create_request(request: Personal):
    new_request = {
        "id": len(personal_db) + 1,
        **request.model_dump(),
    }
    personal_db.append(new_request)
    return request  

@app.get("/personal/")
def get_requests(skip: int = 0, limit: int = 10) -> list[PersonalOut]:
    return personal_db[skip: skip + limit]

@app.get("/personal/{personal_id}")
def get_request(request_id: int):
    for i in range(len(personal_db)):
        if personal_db[i]["id"] == personal_id:
            return personal_db[i]
    return {
        "personal_id": "ID not found"
    }

@app.delete("/personal/{personal_id}")
def delete_request(request_id: int):
    for i in range(len(personal_db)):
        if personal_db[i]["id"] == request_id:
            del personal_db[i]
            break
    else:
        return {"message": "personal ID not found"}
    return {"message": f"personal {personal_id} deleted"}